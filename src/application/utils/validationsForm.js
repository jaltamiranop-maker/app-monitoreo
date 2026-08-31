import {ValidationError} from "../utils/errors"

export function validationsForm(form){
    //Verificacion de campos----------------------------------------------------------------------
    if(form.datos_form.transporte === "Kingspan" && !form.datos_form.servicio_logistico && !form.datos_form.direccion){
        throw new ValidationError(`Campo no completado: ${form.texto_form[13].toUpperCase()}`);
    }
    
    for (const [indice, [valor]] of Object.values(form.datos_form).entries()) {

        const excluir = [5,7,13,14,15]
        if(!excluir.includes(indice) && (!valor || valor == 0) ){
            throw new ValidationError(`Campo no completado: ${form.texto_form[indice].toUpperCase()}`);
        }
    }

    

}