/* eslint-disable @typescript-eslint/no-explicit-any */
import { CSSProperties, useEffect, useState } from "react";
import "./Home.scss";
import Button from "../../components/button/Button";
import { useNavigate } from "react-router-dom";
import axios from "../../util/axios_base";
import { errorNotification } from "../../components/notice/notification";

const buttonStyle: CSSProperties = {
    marginLeft: "65px",

};

const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL;
const ws: WebSocket = new WebSocket(WEBSOCKET_URL + "/ws/1");

const countStatus = (arr: Array<any>) => {
    let tmp = 0;
    for (const item of arr) {
        console.log(item)
        if(item["being"] === true) {
            tmp++;
        }
    }

    return tmp;
}

const convertStatus = (data: any, isClass: boolean) => {
    if(data == true) {
        return isClass? "present" : "在室";
    } else if(data == false) {
        return isClass? "absent" : "不在";
    } else {
        return isClass? "" : "-";
    }
}

const Home = () => {
    const [count, setCount] = useState(0);
    const [data, setData] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
        axios.get("/status/1").then(
            (response) => {                
                const initialCount = countStatus(response.data["status"]);
                setCount(initialCount);
                setData(response.data["status"])
            },
            () => {
                errorNotification("データの取得に失敗しました");
            }
        );
        
        if (ws.readyState === WebSocket.OPEN) {
            ws.send("connect");
          }
      }, []);
    
    ws.onmessage = (event) => {
        const jsonData = JSON.parse(event.data);
        setData(jsonData["status"]);
        setCount(countStatus(jsonData["status"]));
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
                <tbody>
                    <tr>
                        <td>名前</td>
                        <td>ステータス</td>
                    </tr>
                    {
                        data.map((item: any) => {
                            return(
                                <tr>
                                    <td>{item["name"]}</td>
                                    <td className={ convertStatus(item["being"], true) }>{ convertStatus(item["being"], false) }</td>
                                </tr>
                            );
                        })
                    }
                </tbody>
            </table>
        </div>
    );
};

export default Home;