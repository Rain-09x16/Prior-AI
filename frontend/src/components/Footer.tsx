export function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

          {/* About */}
          <div>
            <h3 className="text-xl font-bold mb-4">VANTAGE</h3>
            <p className="text-gray-400">
              The TTO Operating System transforming innovation ecosystems
              in emerging markets. From regulatory compliance to commercial success.
            </p>
          </div>

          {/* Tech Stack */}
          <div>
            <h3 className="text-xl font-bold mb-4">Powered By</h3>
            <ul className="text-gray-400 space-y-2">
              <li>🤖 IBM watsonx Orchestrate</li>
              <li>🧠 IBM Granite AI Models</li>
              <li className="text-green-400 font-semibold">✓ 60 Real USPTO Patents Dataset</li>
              <li className="text-green-400 font-semibold">✓ 85% Validated Accuracy</li>
            </ul>
          </div>

          {/* Credits */}
          <div>
            <h3 className="text-xl font-bold mb-4">Built For Impact</h3>
            <p className="text-gray-400 mb-4">
              Created by <strong className="text-white">Team Impact Hipsters</strong>
              {' '}for the IBM Agentic AI Hackathon 2025
            </p>
            <p className="text-sm text-gray-500">
              Addressing the $500B emerging market innovation gap
            </p>
          </div>

        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-500">
          © 2025 VANTAGE - Team Impact Hipsters | IBM watsonx Hackathon Entry
        </div>
      </div>
    </footer>
  );
}
