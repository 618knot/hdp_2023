import PullDown from "../../components/pulldown/PullDown";
import "./History.scss"


const History = () => {
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
            </table>
        </div>
    );
};

export default History;