import "../styles/components/Field.css"

export default function Field({ label, children, required }) {

    return (

        <div className="field">

            <label className="field-label">

                {label}

                {required && <span className="required">*</span>}

            </label>

            {children}

        </div>

    );

}