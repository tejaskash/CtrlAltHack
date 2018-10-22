using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Web;
using Microsoft.ProjectOxford.Vision;
using Microsoft.ProjectOxford.Vision.Contract;
using codefundo.Services;
namespace codefundo.Service
{
    public class VisionService : ICaptionService
    {
        /// <summary>  
        /// Microsoft Computer Vision API key.  
        /// </summary>  
        private static readonly string ApiKey = "92048d9e18d846b88b57ba296116a07b";

        /// <summary>  
        /// The set of visual features we want from the Vision API.  
        /// </summary>  
        private static readonly VisualFeature[] VisualFeatures = { VisualFeature.Description };

        public async Task<string> GetCaptionAsync(string url)
        {
            var client = new VisionServiceClient(ApiKey, "https://centralindia.api.cognitive.microsoft.com/vision/v1.0");
            var result = await client.AnalyzeImageAsync(url, VisualFeatures);
            return ProcessAnalysisResult(result);
        }
        public async Task<string> GetCaptionAsync(Stream stream)
        {
            var client = new VisionServiceClient(ApiKey, "https://centralindia.api.cognitive.microsoft.com/vision/v1.0");
            var result = await client.AnalyzeImageAsync(stream, VisualFeatures);
            return ProcessAnalysisResult(result);
        }

        /// <summary>  
        /// Processes the analysis result.  
        /// </summary>  
        /// <param name="result">The result.</param>  
        /// <returns>The caption if found, error message otherwise.</returns>  
        private static string ProcessAnalysisResult(AnalysisResult result)
        {
            string message = result?.Description?.Captions.FirstOrDefault()?.Text;

            return string.IsNullOrEmpty(message) ?
                        "Couldn't find a caption for this one" :
                        "I think it's " + message;
        }
    }
}