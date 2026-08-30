import "../styles/components/Select.css"

export default function Select({ className = "",children, ...props }) {
  return (
    <select
      className={`select ${className}`}
      {...props}
    >
      {children}
    </select>
  );
}