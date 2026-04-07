function CitationList({ citations }) {
  if (!citations.length) {
    return null
  }

  return (
    <div className="mt-4 rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <h3 className="m-0 text-sm font-semibold text-gray-800">Sources</h3>

      <div className="mt-3 space-y-3">
        {citations.map((item) => (
          <div key={`${item.file_name}-${item.id}`} className="rounded-lg bg-gray-50 p-3 text-sm">
            <div className="font-medium text-gray-800">
              [{item.id}] {item.file_name} - page {item.page}
            </div>
            <div className="mt-1 text-gray-600">{item.snippet}...</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CitationList
