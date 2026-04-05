/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useState } from "react";
import { useFetchdata } from "../hooks/useFetchdata";
import type { DashDataTypes, AiSuggestionType } from "../types/dashboardTypes";
// SVG Icons
const Icons = {
    Chart: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18" /><path d="m19 9-5 5-4-4-3 3" /></svg>,
    WarningAlert: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><path d="M12 9v4" /><path d="M12 17h.01" /></svg>,
    CheckCircle: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><path d="m9 11 3 3L22 4" /></svg>,
    Search: () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></svg>,
    Bell: () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></svg>,
    User: () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></svg>,
    Sparkles: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" /><path d="M5 3v4" /><path d="M3 5h4" /></svg>,
    Message: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z" /></svg>,
    Download: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" x2="12" y1="15" y2="3" /></svg>,
    Layers: () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2" /><polyline points="2 12 12 17 22 12" /><polyline points="2 17 12 22 22 17" /></svg>,
    Settings: () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" /></svg>,
};

// const clashData = [
//     { id: '#CL-8842', elements: 'HVAC Duct vs. Structural Beam', type: 'HARD', severity: 'HIGH', coords: '12.44, 45.12, -2.50' },
//     { id: '#CL-8843', elements: 'Plumbing Pipe vs. Electrical Tray', type: 'SOFT', severity: 'LOW', coords: '15.20, 30.05, 5.10' },
//     { id: '#CL-8844', elements: 'Sprinkler Line vs. Ceiling Grid', type: 'CLEARANCE', severity: 'MEDIUM', coords: '8.50, 22.10, 3.80' },
//     { id: '#CL-8845', elements: 'Return Air Duct vs. Wall Framing', type: 'HARD', severity: 'HIGH', coords: '2.10, 14.80, -1.20' },
//     { id: '#CL-8846', elements: 'Lighting Fixture vs. HVAC Diffuser', type: 'CLEARANCE', severity: 'MEDIUM', coords: '18.90, 10.40, 4.50' },
//     { id: '#CL-8847', elements: 'Drainage Pipe vs. Steel Column', type: 'HARD', severity: 'HIGH', coords: '25.30, 8.70, -0.50' },
// ];



const Dashboard = () => {
    const [data, setData] = useState<DashDataTypes[]>([])
    const [aiData, setAiData] = useState<AiSuggestionType[]>([])

    const { fetchdata, fetchAiData } = useFetchdata();

    // Dynamic computations for UI
    const totalClashes = data.length;
    const highSeverityCount = data.filter(d => d.severity.toLowerCase() === 'high').length;
    const mediumSeverityCount = data.filter(d => d.severity.toLowerCase() === 'medium').length;
    const lowSeverityCount = data.filter(d => d.severity.toLowerCase() === 'low').length;

    // Additional AI computations
    const clashTypes = data.map(d => d.clash_type);
    const mostCommonType = clashTypes.length > 0 ? clashTypes.sort((a,b) =>
          clashTypes.filter(v => v===a).length
        - clashTypes.filter(v => v===b).length
    ).pop() : 'N/A';
    const mostCommonCount = clashTypes.filter(v => v === mostCommonType).length;
    const mostCommonPercentage = totalClashes > 0 ? Math.round((mostCommonCount / totalClashes) * 100) : 0;


    useEffect(() => {
        const fetch = async () => {
            const d = await fetchdata();
            setData(d || []);
            const ai = await fetchAiData();
            setAiData(ai || []);
        }

        fetch();
    }, []);

    return (
        <div className="bg-zinc-950 min-h-screen text-slate-300 font-sans flex overflow-hidden">
            {/* Sidebar */}
            {/* <aside className="w-64 bg-zinc-900 border-r border-zinc-800 flex-col hidden md:flex shrink-0">
                <div className="p-6">
                    <h2 className="text-white text-xl font-bold flex items-center gap-2">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-lg">N</span>
                        </div>
                        Navix
                    </h2>
                </div>
                <nav className="flex-1 px-4 space-y-2 mt-4">
                    <a href="#" className="flex items-center gap-3 px-3 py-2 bg-zinc-800 rounded-lg text-white">
                        <Icons.Layers /> Dashboard
                    </a>
                    <a href="#" className="flex items-center gap-3 px-3 py-2 hover:bg-zinc-800/50 rounded-lg transition-colors">
                        <Icons.Chart /> Reports
                    </a>
                </nav>
                <div className="p-4 border-t border-zinc-800">
                    <button className="flex items-center gap-2 w-full px-4 py-2 bg-zinc-800 hover:bg-zinc-700 transition-colors rounded-lg text-white text-sm ">
                        <Icons.Settings /> Settings
                    </button>
                </div>
            </aside> */}

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col h-screen overflow-hidden">
                {/* Header Navbar */}
                <header className="h-16 border-b border-zinc-800 flex items-center justify-between px-8 bg-zinc-900/50 shrink-0">
                    <div className="flex items-center gap-8">
                        <nav className="flex items-center gap-6 text-sm font-medium">
                            <a href="#" className="text-blue-500 border-b-2 border-blue-500 h-16 flex items-center">Overview</a>
                            {/* <a href="#" className="hover:text-white transition-colors h-16 flex items-center">Projects</a>
                            <a href="#" className="hover:text-white transition-colors h-16 flex items-center">Models</a>
                            <a href="#" className="hover:text-white transition-colors h-16 flex items-center">Activity</a> */}
                        </nav>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-zinc-500">
                                <Icons.Search />
                            </div>
                            <input
                                type="text"
                                placeholder="Search elements, crashes..."
                                className="bg-zinc-900 border border-zinc-800 rounded-full py-1.5 pl-10 pr-4 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 w-64 text-white"
                            />
                        </div>
                        <button className="text-zinc-400 hover:text-white transition-colors">
                            <Icons.Bell />
                        </button>
                        <button className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600/20 text-blue-500 border border-blue-500/30">
                            <Icons.User />
                        </button>
                    </div>
                </header>

                <main className="flex-1 overflow-y-auto p-8 bg-zinc-950 mx-20 hide-scrollbar">
                    {/* Dashboard Page Header */}
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                        <div>
                            <h1 className="text-3xl font-bold text-white tracking-tight">AI-Based MEP Clash Detection & Rerouting</h1>
                            <p className="mt-1 text-zinc-400">Project: Alpha Tower • Level 4 Coordination • Last scan: 2 hours ago</p>
                        </div>
                        <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-5 py-2.5 rounded-lg font-medium transition-colors shadow-lg shadow-blue-900/20">
                            <Icons.Sparkles /> Run AI Check
                        </button>
                    </div>

                    {/* Summary Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                        <div className="bg-zinc-900/80 backdrop-blur-md border border-zinc-800 rounded-2xl p-6 border-t-[4px] border-t-blue-500 hover:-translate-y-1 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="text-zinc-400 text-xs font-bold uppercase tracking-wider mb-2">Total Clashes</p>
                                    <h3 className="text-4xl font-black text-white tracking-tight">{totalClashes}</h3>
                                </div>
                                <div className="p-2.5 bg-blue-500/10 text-blue-500 rounded-xl">
                                    <Icons.Chart />
                                </div>
                            </div>
                            <p className="text-xs text-zinc-500 mt-5 flex items-center gap-1.5">
                                <span className="text-blue-400 font-medium">Updated live</span> vs source
                            </p>
                        </div>

                        <div className="bg-zinc-900/80 backdrop-blur-md border border-zinc-800 rounded-2xl p-6 border-t-[4px] border-t-red-500 hover:-translate-y-1 hover:shadow-2xl hover:shadow-red-500/10 transition-all duration-300">
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="text-zinc-400 text-xs font-bold uppercase tracking-wider mb-2">High Severity</p>
                                    <h3 className="text-4xl font-black text-white tracking-tight">{highSeverityCount}</h3>
                                </div>
                                <div className="p-2.5 bg-red-500/10 text-red-500 rounded-xl">
                                    <div className="w-5 h-5 flex items-center justify-center font-bold text-lg">!</div>
                                </div>
                            </div>
                            <p className="text-xs text-zinc-500 mt-5 flex items-center gap-1.5">Critical path impact</p>
                        </div>

                        <div className="bg-zinc-900/80 backdrop-blur-md border border-zinc-800 rounded-2xl p-6 border-t-[4px] border-t-amber-500 hover:-translate-y-1 hover:shadow-2xl hover:shadow-amber-500/10 transition-all duration-300">
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="text-zinc-400 text-xs font-bold uppercase tracking-wider mb-2">Medium Severity</p>
                                    <h3 className="text-4xl font-black text-white tracking-tight">{mediumSeverityCount}</h3>
                                </div>
                                <div className="p-2.5 bg-amber-500/10 text-amber-500 rounded-xl">
                                    <Icons.WarningAlert />
                                </div>
                            </div>
                            <p className="text-xs text-zinc-500 mt-5 flex items-center gap-1.5">Requires manual review</p>
                        </div>

                        <div className="bg-zinc-900/80 backdrop-blur-md border border-zinc-800 rounded-2xl p-6 border-t-[4px] border-t-emerald-500 hover:-translate-y-1 hover:shadow-2xl hover:shadow-emerald-500/10 transition-all duration-300">
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="text-zinc-400 text-xs font-bold uppercase tracking-wider mb-2">Low Severity</p>
                                    <h3 className="text-4xl font-black text-white tracking-tight">{lowSeverityCount}</h3>
                                </div>
                                <div className="p-2.5 bg-emerald-500/10 text-emerald-500 rounded-xl">
                                    <Icons.CheckCircle />
                                </div>
                            </div>
                            <p className="text-xs text-zinc-500 mt-5 flex items-center gap-1.5">Soft/Clearance items</p>
                        </div>
                    </div>

                    {/* Data Grid & AI Insights Box */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 pb-20">
                        {/* Left Column: Clash Log Table */}
                        <div className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden shadow-sm flex flex-col">
                            <div className="p-5 border-b border-zinc-800 flex justify-between items-center">
                                <h3 className="text-lg font-bold text-white">Recent Clash Log</h3>
                                {/* <button className="text-sm text-blue-500 hover:text-blue-400 font-medium">View All</button> */}
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left border-collapse ">
                                    <thead>
                                        <tr className="border-b border-zinc-800 text-xs uppercase tracking-wider text-zinc-500 bg-zinc-900/50">
                                            <th className="px-5 py-3 font-medium">Clash ID</th>
                                            <th className="px-5 py-3 font-medium">Elements</th>
                                            <th className="px-5 py-3 font-medium">Type</th>
                                            <th className="px-5 py-3 font-medium">Severity</th>
                                            <th className="px-5 py-3 font-medium">Coordinates</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-sm divide-y divide-zinc-800/50">
                                        {data.map((clash, i) => (
                                            <tr key={i} className="hover:bg-zinc-800/30 transition-colors overflow-y-auto max-h-[20vh]">
                                                <td className="px-5 py-4 align-middle font-medium text-blue-400">{clash.clash_id}</td>
                                                <td className="px-5 py-4 align-middle text-zinc-300">{clash.item1_type} vs {clash.item2_type}</td>
                                                <td className="px-5 py-4 align-middle">
                                                    <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${clash.clash_type === 'Hard' ? 'bg-zinc-800 text-zinc-300 border border-zinc-700' :
                                                        clash.clash_type === 'Soft' ? 'bg-zinc-800/50 text-zinc-400 border border-zinc-700/50' :
                                                            'bg-zinc-800/50 text-zinc-400 border border-zinc-700/50'
                                                        }`}>
                                                        {clash.clash_type}
                                                    </span>
                                                </td>
                                                <td className="px-5 py-4 align-middle">
                                                    <span className={`inline-flex items-center w-20 justify-center px-2 py-1 rounded text-xs font-semibold ${clash.severity === 'High' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                                                        clash.severity=== 'Medium' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                                                            clash.severity === 'Low' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : ''
                                                        }`}>
                                                        {clash.severity}
                                                    </span>
                                                </td>
                                                <td className="px-5 py-4 align-middle text-zinc-500 font-mono text-xs">{clash.x},{clash.y}, {clash.z}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Right Column: AI Insights Panel */}
                        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 shadow-sm flex flex-col">
                            <h3 className="text-zinc-400 text-xs font-bold uppercase tracking-wider mb-4 flex items-center gap-2">
                                <Icons.Sparkles /> AI Insights
                            </h3>

                            <div className="space-y-4 flex-1">
                                <div className="text-sm p-4 bg-zinc-800/20 rounded-xl border border-zinc-800 mb-6">
                                    <p className="text-zinc-400 mb-2 flex justify-between">
                                        <span>Most common clash type:</span>
                                        <strong className="text-white bg-zinc-800 px-2 py-0.5 rounded">{mostCommonType} ({mostCommonPercentage}%)</strong>
                                    </p>
                                    <p className="text-zinc-400 flex justify-between">
                                        <span>High severity clashes:</span>
                                        <strong className="text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20">{highSeverityCount}</strong>
                                    </p>
                                </div>

                                <div className="mt-4 max-h-96 overflow-y-auto pr-2">
                                    {aiData.length > 0 ? (
                                        aiData.map((suggestion, idx) => (
                                            <div key={idx} className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50 mb-3">
                                                <h4 className="text-white font-medium text-sm mb-2 flex items-center gap-2">
                                                    <div className="w-2 h-2 rounded-full bg-blue-500"></div> Suggestion {idx + 1} ({suggestion.action})
                                                </h4>
                                                <p className="text-zinc-400 text-sm leading-relaxed mb-3">
                                                    AI suggests rerouting element <span className="text-blue-400 font-medium">#{suggestion.element_id}</span> for clash <span className="text-white">{suggestion.clash_id}</span>.
                                                </p>
                                                <div className="bg-zinc-900 rounded-lg p-3 text-xs">
                                                    <span className="text-zinc-500 block mb-2 font-semibold">Recommended Rerouting Offset (Δ)</span>
                                                    <div className="flex gap-3">
                                                        <div className={`font-mono px-3 py-1.5 rounded border flex-1 text-center ${suggestion.offsets.x !== 0 ? 'bg-blue-500/10 border-blue-500/20 text-blue-400 font-bold' : 'bg-zinc-800/50 border-zinc-800 text-zinc-500'}`}>
                                                            X: {suggestion.offsets.x > 0 ? '+' : ''}{Number(suggestion.offsets.x.toFixed(3))}
                                                        </div>
                                                        <div className={`font-mono px-3 py-1.5 rounded border flex-1 text-center ${suggestion.offsets.y !== 0 ? 'bg-blue-500/10 border-blue-500/20 text-blue-400 font-bold' : 'bg-zinc-800/50 border-zinc-800 text-zinc-500'}`}>
                                                            Y: {suggestion.offsets.y > 0 ? '+' : ''}{Number(suggestion.offsets.y.toFixed(3))}
                                                        </div>
                                                        <div className={`font-mono px-3 py-1.5 rounded border flex-1 text-center ${suggestion.offsets.z !== 0 ? 'bg-blue-500/10 border-blue-500/20 text-blue-400 font-bold' : 'bg-zinc-800/50 border-zinc-800 text-zinc-500'}`}>
                                                            Z: {suggestion.offsets.z > 0 ? '+' : ''}{Number(suggestion.offsets.z.toFixed(3))}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50 flex items-center justify-center text-zinc-500 text-sm h-32">
                                            No AI suggestions currently available.
                                        </div>
                                    )}
                                </div>

                                <blockquote className="border-l-[3px] border-blue-500 pl-4 py-1 mt-6 bg-blue-500/5 rounded-r-lg">
                                    <p className="text-sm italic text-zinc-300">
                                        "Potential 15% reduction in material waste if Reroute Suggestion #14 is applied to all floor levels."
                                    </p>
                                </blockquote>
                            </div>
                        </div>
                    </div>
                </main>
            </div>

            {/* Floating Support/Chat Button */}
            <button className="absolute bottom-8 right-8 w-14 h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-full flex items-center justify-center shadow-lg shadow-blue-900/50 transition-transform hover:scale-105 z-50">
                <Icons.Message />
            </button>
        </div>
    );
};

export default Dashboard;