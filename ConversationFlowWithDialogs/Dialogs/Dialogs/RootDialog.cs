using System;
using System.Threading.Tasks;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Connector;

namespace Dialogs.Dialogs
{
    [Serializable]
    public class RootDialog : IDialog<object>
    {
        public string name;
        public string age;
        public string color;
        public Task StartAsync(IDialogContext context)
        {
            context.Wait(MessageReceivedAsync);

            return Task.CompletedTask;
        }

        private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<object> result)
        {
            PromptDialog.Text(context, this.NameReceived, "Hi! I am Firebot. Ask me something.");
        }
        private async Task NameReceived(IDialogContext context, IAwaitable<string> result)
        {
            name = await result;
            PromptDialog.Text(context, this.AgeReceived, " Please Enter your area.");

        }
        private async Task AgeReceived(IDialogContext context, IAwaitable<string> result)
        {
            age = await result;
            PromptDialog.Text(context, this.ColorReceived, "Thank you. I am scouring through images of"+age+" to find fires....  I found 1 fire in the area of California. These are its GPS coordinates. 37.7749° N, 122.4194° W");

        }
        private async Task ColorReceived(IDialogContext context, IAwaitable<string>result)
        {
            context.Done<object>(null);
            
            

        }

    }
}