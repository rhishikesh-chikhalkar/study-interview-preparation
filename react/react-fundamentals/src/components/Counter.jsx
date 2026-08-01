import "../App.css";
import { useState } from "react";

const Counter = () => {
  const [count, setCount] = useState(0);
  return (
    <>
      <h1>{count}</h1>
      <div className="button-group">
        <button className="btn-primary" onClick={() => setCount(count + 1)}>
          Increment
        </button>
        <button className="btn-primary" onClick={() => setCount(count - 1)}>
          Decrement
        </button>
        <button className="btn-primary" onClick={() => setCount(0)}>
          Reset
        </button>
      </div>
    </>
  );
};

export default Counter;
