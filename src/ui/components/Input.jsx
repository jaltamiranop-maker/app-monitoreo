import "../styles/components/Input.css"

export default function Input({ className = "", ...props }) {
    return (
        <input
            className={`input ${className}`}
            {...props}
          
        />
    );
}