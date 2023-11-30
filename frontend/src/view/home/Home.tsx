import { CSSProperties, useEffect, useState } from "react";
import "./Home.scss";
import Button from "../../components/button/Button";
import { useNavigate } from "react-router-dom";

const buttonStyle: CSSProperties = {
    marginLeft: "65px",

};

const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL;
const ws: WebSocket = new WebSocket(WEBSOCKET_URL + "/ws/1");

const Home = () => {
    const [count, setCount] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        const intervalId = setInterval(() => {
          // WebSocketサーバーにリクエストを送信
          ws.send("getWebSocketValue");
        }, 3000);
    
        // コンポーネントがアンマウントされたときにクリア
        return () => clearInterval(intervalId);
      }, []);
    
    ws.onmessage = (event) => {
        setCount(event.data);
    }

    return (
        <div className="Home">
            <div id="occupancy">
                <span className="count">{count}</span>名在室
                <Button
                    className="secondary"
                    label="履歴を見る"
                    style={buttonStyle}
                    onClick={ () => navigate("/history") }
                />
            </div>
            <table>
                <tr>
                    <td>名前</td>
                    <td>ステータス</td>
                </tr>
                <tr>
                    <td>研究太郎</td>
                    <td>在室</td>
                </tr>
                <tr>
                    <td>研究次郎</td>
                    <td>不在</td>
                </tr>
            </table>
        </div>
    );
};

export default Home;