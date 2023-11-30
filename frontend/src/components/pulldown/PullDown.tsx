import "./PullDown.scss";

type PullDownProps = {
    name: string;
    options: Array<string>;
};

const PullDown = (props: PullDownProps) => {
    return (
        <>
            <select name={props.name}>
                {props.options.map((element) => (
                    <option>
                        {element}
                    </option>
                ))}
            </select>
        </>
    );
};

export default PullDown;