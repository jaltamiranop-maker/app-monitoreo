import { getNextOrder } from "../services/orderService";
import { useState, useEffect } from "react";

export function useOrder(){
    const [nextOrden, setNextOrden] = useState(1);

    useEffect(() => {
        const loadNextOrder = async() => {

                const data = await getNextOrder();

                if(data){
                    setNextOrden(data.siguiente);
                }

            
            }
        loadNextOrder();
    }, []);

    
    const handleOrdenSaved = () => {
        setNextOrden(n => n + 1);
    };


    return {
        nextOrden,
        handleOrdenSaved
    };
    
    



}