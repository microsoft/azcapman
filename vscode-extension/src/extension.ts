import * as vscode from 'vscode';
import { SYSTEM_PROMPT, getCommandContext } from './prompts.js';

const PARTICIPANT_ID = 'azure-capacity-manager.agent';

export function activate(context: vscode.ExtensionContext): void {
    const participant = vscode.chat.createChatParticipant(PARTICIPANT_ID, requestHandler);
    context.subscriptions.push(participant);
}

const requestHandler: vscode.ChatRequestHandler = async (
    request: vscode.ChatRequest,
    context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
): Promise<vscode.ChatResult> => {
    const commandContext = getCommandContext(request.command);
    const fullSystemPrompt = commandContext
        ? `${SYSTEM_PROMPT}\n\n## Current task focus\n\n${commandContext}`
        : SYSTEM_PROMPT;

    const messages: vscode.LanguageModelChatMessage[] = [
        vscode.LanguageModelChatMessage.User(fullSystemPrompt),
    ];

    // Replay conversation history so the model has continuity across turns
    for (const historyItem of context.history) {
        if (historyItem instanceof vscode.ChatRequestTurn) {
            messages.push(vscode.LanguageModelChatMessage.User(historyItem.prompt));
        } else if (historyItem instanceof vscode.ChatResponseTurn) {
            const text = historyItem.response
                .filter((p): p is vscode.ChatResponseMarkdownPart =>
                    p instanceof vscode.ChatResponseMarkdownPart
                )
                .map(p => p.value.value)
                .join('');
            if (text) {
                messages.push(vscode.LanguageModelChatMessage.Assistant(text));
            }
        }
    }

    messages.push(vscode.LanguageModelChatMessage.User(request.prompt));

    const response = await request.model.sendRequest(messages, {}, token);
    for await (const fragment of response.text) {
        stream.markdown(fragment);
    }

    return {};
};

export function deactivate(): void { /* empty */ }
