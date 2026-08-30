import { useEffect } from "react";
import "../styles/components/Toast.css";

export default function Toast({ message, type, onClose }) {

    useEffect(() => {

        const timer = setTimeout(onClose, 3500);

        return () => clearTimeout(timer);

    }, [onClose]);

    return (

        <div className={`toast toast${type}`}>

            {type === "success" && <IconCheck />}

            <span>{message}</span>

        </div>

    );

}