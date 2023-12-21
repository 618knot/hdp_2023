import "./PullDown.scss";

type PullDownProps = {
    name: string;
    options: Array<string>;
    value: string;
    setValue: React.Dispatch<React.SetStateAction<string>>;
};

const PullDown = (props: PullDownProps) => {
    return (
        <select value={ props.value } name={props.name} onChange={ (event) => {
            props.setValue(event.target.value);
        } }>
            {props.options.map((element) => (
                <option value={element}>
                    {element}
                </option>
            ))}
        </select>
    );
};

export default PullDown;