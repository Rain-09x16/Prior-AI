'use client';

import { useRouter } from 'next/navigation';
import { FileUpload } from '@/components/FileUpload';
import { useAnalysisStore } from '@/stores/analysisStore';
import { Sparkles, TrendingUp, Clock, Shield } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();
  const createAnalysis = useAnalysisStore((state) => state.createAnalysis);

  const handleUpload = async (file: File) => {
    try {
      const analysisId = await createAnalysis(file);
      router.push(`/analyses/${analysisId}`);
    } catch (error) {
      console.error('Upload failed:', error);
      throw error;
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-blue-50 to-white py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              AI-Powered Prior Art Analysis
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Reduce patent prior art analysis from 10-15 hours to 15 minutes using
              advanced AI and machine learning
            </p>
          </div>

          {/* Upload Section */}
          <div className="mb-12">
            <FileUpload onUpload={handleUpload} />
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            <div className="bg-white p-6 rounded-lg border border-gray-200 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
                <Sparkles className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">AI-Powered</h3>
              <p className="text-sm text-gray-600">
                Advanced NLU and ML algorithms for accurate claim extraction
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mb-4">
                <Clock className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Save Time</h3>
              <p className="text-sm text-gray-600">
                Complete analysis in minutes instead of hours
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mb-4">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Smart Recommendations</h3>
              <p className="text-sm text-gray-600">
                Get actionable recommendations based on novelty scores
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200 text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-orange-100 rounded-lg mb-4">
                <Shield className="h-6 w-6 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Comprehensive</h3>
              <p className="text-sm text-gray-600">
                Search multiple patent databases and generate detailed reports
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>

          <div className="max-w-4xl mx-auto">
            <div className="space-y-8">
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Upload Disclosure
                  </h3>
                  <p className="text-gray-600">
                    Upload your invention disclosure document (PDF or DOCX format)
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    AI Analysis
                  </h3>
                  <p className="text-gray-600">
                    Our AI extracts claims, searches patent databases, and scores similarity
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Review Results
                  </h3>
                  <p className="text-gray-600">
                    Get novelty scores, recommendations, and detailed patent comparisons
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                  4
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Generate Report
                  </h3>
                  <p className="text-gray-600">
                    Download a comprehensive PDF report for your records
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
