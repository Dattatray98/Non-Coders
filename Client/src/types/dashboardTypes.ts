export interface DashDataTypes {
    clash_id: string,
    item1_id: string,
    item1_type: string,
    item2_id: string,
    item2_type: string,
    clash_type:string,
    severity:string,
    x:number,
    y:number,
    z:number
}

export interface AiSuggestionType {
    clash_id: string,
    element_id: string,
    action: string,
    new_position: {
        x: number,
        y: number,
        z: number
    },
    offsets: {
        x: number,
        y: number,
        z: number
    }
}