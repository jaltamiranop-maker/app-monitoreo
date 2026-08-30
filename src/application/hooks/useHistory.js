import { useEffect, useState } from "react";
import {
    getHistory,
    regeneratePDF
} from "../services/historyService"

export function useHistory(){
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [regenId, setRegenId] = useState("");
    const [toast, setToast] = useState(null);

    const fetchHistory = async () => {
    setLoading(true);

    try {
      const data = await getHistory();
      setHistory(data);
    } catch (error){
        setToast({
            message:error.message,
            type: "-error",
        });
    } finally {
        setLoading(false);
    }

    };

    const handleRegen = async () => {
    if (!regenId) return;
    try {
        
        
      const blob = await regeneratePDF(regenId);

      const url = URL.createObjectURL(blob);

      const a = document.createElement("a"); 
      a.href = url; 
      a.download = `Orden_${regenId}.pdf`; 
      a.click();

      URL.revokeObjectURL(url);

      setToast({ 
        message: `PDF de la orden #${regenId} descargado.`, 
        type: "-success" 
    });
    
    } catch (error) {
      setToast({ 
        message: `Error: ${error.message}`, 
        type: "-error" 
    });
    
    }
  };
  useEffect(() => {
    fetchHistory();
    }, []);

    return {

        history,
        loading,
        regenId,
        setRegenId,
        toast,
        setToast,
        handleRegen,
    };

}