import PullDown from "../../components/pulldown/PullDown";
import "./History.scss";
import axios from "../../util/axios_base";
import { useEffect, useState } from "react";



const History = () => {
    const [data, setData] = useState([]);
    useEffect(() => {
        // eslint-disable-next-line react-hooks/exhaustive-deps
        axios.get("/history/1").then(
            (response) => {
                setData(response.data["history"]);
            }
        );
    }, []);

    return (
        <div className="History">
            <h2>履歴</h2>
            <div className="select">
                <PullDown
                    name="member"
                    options={
                        ["全員", "研究太郎", "研究次郎"]
                    }
                />
            </div>
            <table>
                <tr>
                    <td className="time">2023/11/30 10:26</td>
                    <td className="status">退室</td>
                    <td className="name">研究太郎</td>
                </tr>
                <tr>
                    <td className="time">2023/11/30 10:26</td>
                    <td className="status">入室</td>
                    <td className="name">研究次郎</td>
                    
                </tr>
                {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    data.map((item: any) => {
                        return (
                            <tr>
                                <td className="time">{item["time"]}</td>
                                <td className="status">{item["status"] ? "入室" : "退室"}</td>
                                <td className="name">{item["user"]}</td>
                            </tr>
                        );
                    })
                }
            </table>
        </div>
    );
};

export default History;