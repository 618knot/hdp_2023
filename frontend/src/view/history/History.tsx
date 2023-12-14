import PullDown from "../../components/pulldown/PullDown";
import "./History.scss";
import axios from "../../util/axios_base";
import { useEffect, useState } from "react";

const History = () => {
    const [data, setData] = useState([]);
    const [selectValue, setSelectValue] = useState("全員");
    
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
                        ["全員", "研究 太郎", "研究 次郎"]
                    }
                    value={selectValue}
                    setValue={ setSelectValue }
                    key={selectValue}
                />
            </div>
            <table>
                {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    data.map((item: any) => {
                        if (selectValue == "全員") {
                            return (
                                <tr>
                                    <td className="time">{item["time"]}</td>
                                    <td className="status">{item["status"] ? "入室" : "退室"}</td>
                                    <td className="name">{item["user"]}</td>
                                </tr>
                            );
                        }else if (item["user"] == selectValue) {
                            return (
                                <tr>
                                    <td className="time">{item["time"]}</td>
                                    <td className="status">{item["status"] ? "入室" : "退室"}</td>
                                    <td className="name">{item["user"]}</td>
                                </tr>
                            );
                        }
                    })
                }
            </table>
        </div>
    );
};

export default History;