# Next.js Caching Architecture & HTTP Headers

## Overview & Core Concepts

Next.js 15 and 16 introduce a fundamental shift in server-side caching architecture.
Earlier App Router versions (Next.js 13 and 14) relied on aggressive implicit caching
where `fetch` requests and Route Handlers were cached by default.

In modern Next.js releases (15+ and 16 Canary), the framework adopts a **dynamic by default**
and **explicit opt-in caching** model known as **Cache Components**. Developers gain fine-grained
control over cache lifecycles using the `"use cache"` directive, `cacheLife` profiles,
`cacheTag` keys, and predictable HTTP `Cache-Control` header orchestration.

---

## The Next.js Caching Layers

Next.js orchestrates four distinct caching mechanisms:

| Cache Layer | Location | Purpose | Lifetime / Invalidation |
| :--- | :--- | :--- | :--- |
| **Request Memoization** | Server Memory (per-request) | Deduplicates identical `fetch` calls in one render pass | Lifecycle of a single server request |
| **Data Cache / Cache Components** | Server / Shared KV Storage | Caches data across user requests and deployments | Controlled via `"use cache"`, `cacheLife`, and `cacheTag` |
| **Full Route Cache (Prerender)** | Server / CDN Edge | Caches rendered HTML and React Server Component (RSC) payload | Invalidation via tag/path revalidation or build |
| **Client Router Cache** | Client Browser Memory | Stores RSC payloads during in-app navigation | Controlled via `staleTimes` configuration |

---

## Enabling Cache Components

To utilize the modern `"use cache"` directive and unified `cacheLife` profiles, enable
`cacheComponents` (or `dynamicIO` in experimental flags) in `next.config.ts`:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Enables the "use cache" directive and cacheLife profiles
  cacheComponents: true,
  experimental: {
    // Controls client-side Router Cache staleness (in seconds)
    staleTimes: {
      dynamic: 0,
      static: 300,
    },
  },
}

export default nextConfig
```

---

## Core Primitives: `"use cache"`, `cacheLife`, and `cacheTag`

### 1. The `"use cache"` Directive
The `"use cache"` directive tells Next.js to serialize and store the return value of an async
function or component.

- **Placement**: Placed at the top of a file, component, or async function.
- **Dynamic Boundary Isolation**: Cached functions cannot directly read dynamic context
  (e.g., `cookies()`, `headers()`, `searchParams`) inside the cached scope. Dynamic values
  must be passed as arguments.

### 2. `cacheLife` Lifetime Configuration
`cacheLife` sets the time-to-live and revalidation thresholds for cached entries. Next.js
provides default profiles:
- `seconds`: Quick updates (stale ~10s, revalidate ~1m).
- `minutes`: Short-lived data (stale ~5m, revalidate ~1h).
- `hours`: Stable data (stale ~1h, revalidate ~1d).
- `days`: Infrequent changes (stale ~1d, revalidate ~1w).
- `weeks`: Static datasets (stale ~1w, revalidate ~30d).
- `max`: Long-term immutable caching.

### 3. `cacheTag` and Cache Invalidation
- **`cacheTag(string, ...)`**: Associates tags with cached entries.
- **`updateTag(tag)`**: Server Action primitive for instant on-demand cache purge (read-your-own-writes).
- **`revalidateTag(tag)`**: Background revalidation across distributed edge instances.

---

## HTTP `Cache-Control` Headers & Edge CDN Behavior

Next.js emits specific HTTP response headers depending on route dynamics and caching configuration:

### 1. Dynamic Responses (Default in Next.js 15+)
When a route reads dynamic request headers (`cookies()`, `headers()`) or lacks caching:
```http
Cache-Control: private, no-cache, no-store, max-age=0, must-revalidate
```
Browsers and intermediate CDNs will not store the response.

### 2. Static and Cached Responses (`"use cache"` / `force-static`)
When a route or component uses `"use cache"` with `cacheLife('hours')`:
```http
Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400
```
- **`s-maxage=3600`**: Shared caches (CDNs) serve this response fresh for 1 hour.
- **`stale-while-revalidate=86400`**: After 1 hour, CDNs serve stale data while revalidating
  in the background for up to 24 hours.

### 3. Route Handlers Manual Headers
You can customize or override HTTP headers directly in Route Handlers:

```typescript
// app/api/products/route.ts
import { NextResponse } from 'next/server'
import { getCachedProducts } from '@/lib/data-access/products'

export async function GET() {
  const products = await getCachedProducts()

  return NextResponse.json(products, {
    status: 200,
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
      'CDN-Cache-Control': 'public, s-maxage=3600',
      'Vercel-CDN-Cache-Control': 'public, s-maxage=86400',
    },
  })
}
```

---

## End-to-End Implementation Example

### 1. Data Access Layer (`lib/data-access/products.ts`)

```typescript
import { cacheLife, cacheTag } from 'next/cache'

export interface Product {
  id: string
  name: string
  price: number
  inStock: boolean
}

// Cached function: isolated data fetcher
export async function getCachedProducts(): Promise<Product[]> {
  'use cache'
  cacheLife('hours')
  cacheTag('products-list')

  // Simulate database query or third-party service fetch
  const response = await fetch('https://api.example.com/products', {
    headers: { 'Content-Type': 'application/json' },
  })

  if (!response.ok) {
    throw new Error('Failed to retrieve products from upstream service')
  }

  return response.json()
}

// Single item cache by identifier
export async function getCachedProductById(id: string): Promise<Product | null> {
  'use cache'
  cacheLife('days')
  cacheTag(`product-${id}`)

  const response = await fetch(`https://api.example.com/products/${id}`)
  if (response.status === 404) return null
  if (!response.ok) throw new Error(`Failed to retrieve product ${id}`)

  return response.json()
}
```

### 2. Server Action for Invalidation (`lib/actions/products.ts`)

```typescript
'use server'

import { revalidateTag, updateTag } from 'next/cache'

export async function mutateProductPrice(productId: string, newPrice: number) {
  // Perform write operation to database
  await fetch(`https://api.example.com/products/${productId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ price: newPrice }),
  })

  // Purge specific product and product list caches
  updateTag(`product-${productId}`)
  revalidateTag('products-list')
}
```

### 3. Server Component with Suspense (`app/products/page.tsx`)

```typescript
import { Suspense } from 'react'
import { getCachedProducts } from '@/lib/data-access/products'

async function ProductList() {
  const products = await getCachedProducts()

  return (
    <ul>
      {products.map((item) => (
        <li key={item.id}>
          <span>{item.name}</span> - <span>${item.price.toFixed(2)}</span>
        </li>
      ))}
    </ul>
  )
}

export default function ProductsPage() {
  return (
    <main>
      <h1>Product Catalog</h1>
      <Suspense fallback={<p>Loading product catalog...</p>}>
        <ProductList />
      </Suspense>
    </main>
  )
}
```

---

## Common Pitfalls & Best Practices

1. **Do Not Call Dynamic APIs Inside `"use cache"`**:
   Calling `cookies()`, `headers()`, or accessing non-deterministic values (like `Math.random()`
   or `Date.now()`) inside a `"use cache"` function causes build errors or cache poisoning.
   Pass required dynamic values (e.g., `userId`) as function arguments.

2. **Differentiate `updateTag` and `revalidateTag`**:
   - Use `updateTag(tag)` inside Server Actions when the user expects immediate visual reflection
     (read-your-own-writes).
   - Use `revalidateTag(tag)` in webhooks or Route Handlers for background propagation.

3. **Avoid Duplicating Cache Rules**:
   Do not mix `export const revalidate = 60` route segment config with `cacheLife('minutes')`.
   Standardize on `"use cache"` and `cacheLife`.

---

# Interview Questions & Answers (5 YOE Level)

## 1. Conceptual / Theoretical

### Question:
How does the caching philosophy in Next.js 15+ and 16 differ from Next.js 13/14? Explain the
role of Cache Components (`"use cache"`) versus legacy `fetch({ next: { revalidate } })`.

### Answer:
Next.js 13/14 introduced the App Router with implicit, aggressive caching defaults:
- `fetch` requests were cached indefinitely (`force-cache`) by default.
- Client-side Router Cache cached dynamic pages for 30 seconds and static pages for 5 minutes.
- Route Handlers with `GET` requests without dynamic functions were statically cached.

This led to unexpected stale data bugs and developer confusion.

Next.js 15+ reverses this model to **dynamic by default**:
- Unconfigured `fetch` requests and Route Handlers evaluate per-request (`no-store`).
- Caching is made explicit through the `"use cache"` directive at the component or function level.
- `cacheLife()` replaces hardcoded revalidation integers with semantic profiles that control
  client, CDN, and server stale-while-revalidate lifetimes uniformly.
- It decouples data caching from the network layer (`fetch`), allowing database queries,
  SDK calls, and CPU-bound computations to be cached identically.

### Follow-up Questions an Interviewer Might Ask:
- What happens under the hood when a function with `"use cache"` executes?
  *(Answer: Next.js serializes function arguments as a cache key, hashes them with the build ID
  and deployment ID, and stores the resolved payload in the configured Data Cache adapter).*

---

## 2. Practical / Scenario-Based

### Question:
Your team has an e-commerce product page. The page contains global product details (rarely changing),
personalized user recommendations (dynamic per user session), and live inventory count (changes
frequently). How would you architect this page in Next.js 16 to maximize edge caching without
leaking user data or displaying stale inventory?

### Answer:
1. **Global Product Details (Static Cache)**:
   Extract product info into a helper function marked with `"use cache"` and `cacheLife('days')`,
   tagged with `cacheTag('product-${id}')`.
2. **Personalized Recommendations (Private Dynamic)**:
   Extract user preferences via `cookies()` outside the cached function and pass the `userId`
   as an argument to a user-specific cached helper or render it dynamically within a `<Suspense>`
   boundary.
3. **Live Inventory (Frequent Cache / Dynamic)**:
   Use `"use cache"` with `cacheLife('seconds')` or fetch client-side via SWR/TanStack Query.
4. **Composition with Suspense**:
   Wrap the personalized and live inventory sections in React `<Suspense>` boundaries. The outer
   shell streams instantly from the Edge CDN cache (`stale-while-revalidate`), while dynamic
   islands resolve independently.

### Follow-up Questions an Interviewer Might Ask:
- If a user triggers a checkout mutation, how do you ensure the inventory count updates
  immediately for that user while remaining efficient for everyone else?
  *(Answer: Call `updateTag('inventory-${id}')` in the Server Action).*

---

## 3. Coding / Implementation

### Question:
Write a Next.js 16 Route Handler (`app/api/market-summary/route.ts`) that fetches financial data
from a slow upstream database query. The endpoint must cache data for 10 minutes at the CDN
layer with 1 hour stale-while-revalidate window, support on-demand cache eviction via a secret
webhook, and return standard JSON.

### Answer:

```typescript
// lib/data-access/market.ts
import { cacheLife, cacheTag } from 'next/cache'

export interface MarketSummary {
  updatedAt: string
  totalVolume: number
  topGainers: Array<{ symbol: string; change: number }>
}

export async function getMarketSummary(): Promise<MarketSummary> {
  'use cache'
  cacheLife('minutes')
  cacheTag('market-summary-tag')

  // Simulated expensive aggregation query
  return {
    updatedAt: new Date().toISOString(),
    totalVolume: 48920100,
    topGainers: [
      { symbol: 'AAPL', change: 2.4 },
      { symbol: 'GOOGL', change: 1.8 },
    ],
  }
}
```

```typescript
// app/api/market-summary/route.ts
import { NextResponse, type NextRequest } from 'next/server'
import { revalidateTag } from 'next/cache'
import { getMarketSummary } from '@/lib/data-access/market'

export async function GET() {
  try {
    const data = await getMarketSummary()
    return NextResponse.json(data, {
      status: 200,
      headers: {
        'Cache-Control': 'public, s-maxage=600, stale-while-revalidate=3600',
      },
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to retrieve market summary' },
      { status: 500 }
    )
  }
}

// Webhook endpoint for on-demand invalidation
export async function POST(request: NextRequest) {
  const secret = request.headers.get('x-revalidate-secret')
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })
  }

  revalidateTag('market-summary-tag')
  return NextResponse.json({ revalidated: true, timestamp: Date.now() })
}
```

---

## 4. System Design / Architecture

### Question:
In a multi-region Next.js deployment deployed behind Cloudflare / Fastly CDN, describe how HTTP
caching headers (`s-maxage`, `stale-while-revalidate`, `Surrogate-Control`), CDN cache keys,
and Next.js server-side cache tags interact during a rolling deployment or flash sale.

### Answer:
1. **Header Hierarchy & Negotiation**:
   - Next.js emits `Cache-Control: public, s-maxage=X, stale-while-revalidate=Y` which instructs
     intermediate CDN edge POPs how long to serve cached HTML/JSON payloads.
   - For granular CDN control, `CDN-Cache-Control` or `Cloudflare-CDN-Cache-Control` headers can be
     dispatched to dictate edge TTLs independently from browser max-age.
2. **Cache Key Composition**:
   - CDN cache keys are constructed from `Host`, `Path`, `Query String`, and custom variant
     headers (such as `Accept-Encoding: gzip/br` and `x-nextjs-data`).
   - In Next.js, RSC payloads are fetched with `_rsc` headers or query parameters, creating separate
     edge cache slots for raw RSC streams versus compiled HTML documents.
3. **Atomic Deployments & Deployment ID**:
   - Each build produces an immutable `deploymentId` / `buildId`.
   - Asset URLs and RSC queries include this build identifier. When a new deployment is promoted,
     traffic seamlessly switches to new edge artifacts, preventing cache poisoning from old bundles.
4. **On-Demand Edge Invalidation via Tagging**:
   - Enterprise setups bridge `cacheTag()` with CDN Surrogate Keys (e.g., `Surrogate-Key` or
     Cloudflare `Cache-Tag` headers).
   - Calling `revalidateTag()` triggers an API call to the CDN's cache purge endpoint, evicting
     the tagged resource across all global edge nodes simultaneously within milliseconds.
