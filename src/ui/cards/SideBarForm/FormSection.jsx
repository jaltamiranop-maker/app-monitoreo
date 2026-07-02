import SectionHeader from "../../components/SectionHeader"
import "../../styles/cards/SideBarForm/SideBarForm.css"
export default function FormSection({ title, children }){

    return(

        <section>

            <SectionHeader>

                {title}

            </SectionHeader>

            <div className="form-group">

                {children}

            </div>

        </section>

    )

}