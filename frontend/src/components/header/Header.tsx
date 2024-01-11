import { useEffect, useState } from "react";
import "./Header.scss";
import { useNavigate } from "react-router-dom";

const Header = () => {
    const [time, setTime] = useState("");
    const [now, setNow] = useState(new Date());
    const navigate = useNavigate();
    useEffect(() => {
        const timerId = setInterval(() => {
            setNow(new Date());
        }, 1000);

        const year = now.getFullYear();
        const month = now.getMonth() + 1;
        const day = now.getDay();
        const hour = now.getHours().toString().padStart(2, "0");
        const minute = now.getMinutes().toString().padStart(2, "0");
        const second = now.getSeconds().toString().padStart(2, "0");

        setTime(year + "年" + month + "月" + day + "日 " + hour + ":" + minute + ":" + second);

        return () => clearInterval(timerId);
    }, [now]);

    return(
        <header>
            <div className="name">
                <span className="lab-name" onClick={ () => navigate("/") }>
                    HOGE研究室
                </span>
            </div>
            <div className="time">
                {time}
            </div>
        </header>
    );
};

export default Header;