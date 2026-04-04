const data = [
    {id:1},
    {id:2},
    {id:3},
    {id:4}
]


const Dashboard = () => {

    return (
        <div className="bg-black h-screen">
            <div>
                <nav className="h-15 w-full border border-white">

                </nav>
                <div className="h-[93.4vh] border border-yellow-800 flex">
                    <div className="border border-red-800 h-full w-[25%]">

                    </div>
                    <div className="border border-gray-500 h-full w-[75%]">
                        <div className="h-40">
                            <h1 className="text-4xl text-white">AI-Based MEP Clash Detection & Rerouting System</h1>
                        </div>
                        <div className="border border-red-700 h-80">
                            {data.map((item)=>(
                                <div key={item.id} className="flex border border-white">

                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default Dashboard