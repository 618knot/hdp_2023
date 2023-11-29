import './Button.scss';
import { CSSProperties, ReactElement } from 'react';
type ButtonProps = {
    label: string;
    className: string;
    id?: string;
    style?: CSSProperties;
    leftIcon?: ReactElement;
    rightIcon?: ReactElement;
    onClick?: () => void;
};

const Button = (props :ButtonProps) => {
    return (
        <button
            className={`button ${props.className}`}
            id={props.id}
            onClick={props.onClick}
            style={props.style}
        >
            {props.rightIcon}
            {props.label}
            {props.leftIcon}
        </button>
    );
};

export default Button;