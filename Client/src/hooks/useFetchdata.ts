import axios from "axios"

export const useFetchdata = () => {
    const fetchdata = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/clash/data")

            console.log(response.data)
            return response.data
            
        } catch (error) {
            console.error(error)
            return []
        }
    }

    return {fetchdata}
}