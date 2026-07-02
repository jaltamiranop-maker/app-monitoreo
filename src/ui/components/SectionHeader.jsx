import "../styles/components/SectionHeader.css"
export default function SectionHeader({ children }) {
  return (
    <div className="sectionHeader">
      {children}
    </div>
  );
}