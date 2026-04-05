using System;
using System.IO;
using System.Collections.Generic;
using System.Text.Json; // Native C# JSON parser
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.Attributes;

namespace AutoMEPRouter
{
    /// <summary>
    /// C# Revit Add-in Command to execute AI-based rerouting suggestions
    /// </summary>
    [Transaction(TransactionMode.Manual)]
    public class ApplyReroutesCommand : IExternalCommand
    {
        // Internal C# Classes mapping strictly to our project.md and Python JSON structure
        public class RerouteSuggestion
        {
            public string clash_id { get; set; }
            public string element_id { get; set; }
            public string action { get; set; }
            public Offsets offsets { get; set; }
        }

        public class Offsets 
        { 
            public double x { get; set; } 
            public double y { get; set; } 
            public double z { get; set; } 
        }

        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            Document doc = commandData.Application.ActiveUIDocument.Document;

            // Connects to the pipeline output folder from our architecture
            string folderPath = @"\\192.168.12.90\RevitShared";
            string filePath = Path.Combine(folderPath, "ai_reroutes.json");

            if (!File.Exists(filePath))
            {
                TaskDialog.Show("AI MEP Router", "No AI reroute suggestions found! Please run the Python Watchdog pipeline first.");
                return Result.Failed;
            }

            try
            {
                string jsonString = File.ReadAllText(filePath);
                
                // Parse the pipeline's JSON output
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                var suggestions = JsonSerializer.Deserialize<List<RerouteSuggestion>>(jsonString, options);

                int successCount = 0;

                // Open Revit API wrapper enforcing that rollback will safely occur if calculations break
                using (Transaction t = new Transaction(doc, "Apply AI MEP Rerouting"))
                {
                    t.Start();

                    foreach (var suggestion in suggestions)
                    {
                        if (string.IsNullOrEmpty(suggestion.element_id)) continue;

                        if (int.TryParse(suggestion.element_id, out int elemIdVal))
                        {
                            // 1. Find Element by ID
                            ElementId elemId = new ElementId(elemIdVal);
                            Element element = doc.GetElement(elemId);

                            if (element != null && suggestion.action.Contains("move"))
                            {
                                // 2. Apply Movement (Z + offset)
                                // Extract the generated Offset (Converting millimeter output to Revit Internal Feet)
                                double dx = suggestion.offsets.x / 304.8;
                                double dy = suggestion.offsets.y / 304.8;
                                double dz = suggestion.offsets.z / 304.8;

                                if (dx != 0 || dy != 0 || dz != 0)
                                {
                                    // 3. Model Updates in 3D
                                    XYZ translation = new XYZ(dx, dy, dz);
                                    ElementTransformUtils.MoveElement(doc, elemId, translation);
                                    successCount++;
                                }
                            }
                        }
                    }

                    // Solidify logic immediately triggering graphical refresh
                    t.Commit();
                }

                TaskDialog.Show("AI MEP Router", $"Successfully applied {successCount} automated resolutions to the 3D model!");
                return Result.Succeeded;
            }
            catch (Exception ex)
            {
                message = "Pipeline Execution Failed: " + ex.Message;
                return Result.Failed;
            }
        }
    }
}