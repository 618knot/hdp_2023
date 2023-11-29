import { useState } from "react";
const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL;
console.log(WEBSOCKET_URL);
const ws: WebSocket = new WebSocket(WEBSOCKET_URL + "/ws/1");

const Home = () => {
    const [count, setCount] = useState(0);

    setInterval(() => {
                // WebSocketサーバーにリクエストを送信
                ws.send("getWebSocketValue");
            }, 3000);

    ws.onmessage = (event) => {
        setCount(event.data);
    }

    return (
        <>
            <h1>
                {count}
            </h1>
            <h3>名在室</h3>
        </>
    );
};

export default Home;