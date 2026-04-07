function ChatMessage({ role, text }) {
  const isUser = role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-xl px-4 py-3 text-sm leading-6 shadow-sm ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-800 border border-gray-200'
        }`}
      >
        {text}
      </div>
    </div>
  )
}

export default ChatMessage
