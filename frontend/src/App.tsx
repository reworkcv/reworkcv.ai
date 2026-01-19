import { useState, useEffect } from 'react'
import { Sparkles, FileText, Briefcase, Zap, Github } from 'lucide-react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Textarea } from './components/ui/textarea'
import { Label } from './components/ui/label'
import { FileUpload } from './components/FileUpload'
import { PDFPreview } from './components/PDFPreview'
import { ProcessingStatus } from './components/ProcessingStatus'
import { processResume, getPdfPreviewUrl, getPdfDownloadUrl } from './lib/api'

type ProcessingState = 'idle' | 'processing' | 'success' | 'error'

function App() {
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [processingState, setProcessingState] = useState<ProcessingState>('idle')
  const [progress, setProgress] = useState(0)
  const [statusMessage, setStatusMessage] = useState('')
  const [pdfUrl, setPdfUrl] = useState<string | null>(null)
  const [requestId, setRequestId] = useState<string | null>(null)

  const canProcess = resumeFile && jobDescription.trim().length > 50

  useEffect(() => {
    let interval: NodeJS.Timeout
    if (processingState === 'processing') {
      interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) return prev
          return prev + Math.random() * 10
        })
      }, 500)
    }
    return () => clearInterval(interval)
  }, [processingState])

  const handleProcess = async () => {
    if (!resumeFile || !jobDescription) return

    setProcessingState('processing')
    setProgress(0)
    setStatusMessage('Starting processing...')
    setPdfUrl(null)

    try {
      setStatusMessage('Uploading documents...')
      setProgress(10)

      const result = await processResume(resumeFile, jobDescription)

      if (result.success && result.pdf_url) {
        setProgress(100)
        setStatusMessage('Resume tailored successfully!')
        setProcessingState('success')
        
        // Extract request ID from URL
        const id = result.pdf_url.split('/').pop() || ''
        setRequestId(id)
        setPdfUrl(getPdfPreviewUrl(id))
      } else {
        throw new Error(result.message || 'Failed to process resume')
      }
    } catch (error) {
      setProcessingState('error')
      setStatusMessage(error instanceof Error ? error.message : 'An error occurred')
    }
  }

  const handleDownload = () => {
    if (requestId) {
      window.open(getPdfDownloadUrl(requestId), '_blank')
    }
  }

  const handleReset = () => {
    setResumeFile(null)
    setJobDescription('')
    setProcessingState('idle')
    setProgress(0)
    setStatusMessage('')
    setPdfUrl(null)
    setRequestId(null)
  }

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-primary rounded-lg">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
              Resume Tailor
            </span>
          </div>
          <nav className="flex items-center gap-4">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-12 md:py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-primary to-blue-600 bg-clip-text text-transparent">
            Tailor Your Resume with AI
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Upload your resume and job description. Our AI will optimize your resume 
            to match the job requirements and generate a professional PDF.
          </p>
          
          {/* Features */}
          <div className="flex flex-wrap justify-center gap-6 mb-12">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <FileText className="w-4 h-4 text-primary" />
              <span>PDF & DOCX Support</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Briefcase className="w-4 h-4 text-primary" />
              <span>Job-Specific Optimization</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Zap className="w-4 h-4 text-primary" />
              <span>Instant PDF Generation</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 pb-20">
        {pdfUrl && processingState === 'success' ? (
          /* PDF Preview View */
          <div className="max-w-5xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Your Tailored Resume</h2>
              <Button variant="outline" onClick={handleReset}>
                Create Another
              </Button>
            </div>
            <PDFPreview pdfUrl={pdfUrl} onDownload={handleDownload} />
          </div>
        ) : (
          /* Upload Form View */
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              {/* Resume Upload */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-primary" />
                    Upload Resume
                  </CardTitle>
                  <CardDescription>
                    Upload your current resume in PDF or DOCX format
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <FileUpload
                    file={resumeFile}
                    onFileChange={setResumeFile}
                    accept={{
                      'application/pdf': ['.pdf'],
                      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
                      'application/msword': ['.doc'],
                    }}
                    label="Drop your resume here"
                    description="PDF or DOCX, max 10MB"
                  />
                </CardContent>
              </Card>

              {/* Job Description */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Briefcase className="w-5 h-5 text-primary" />
                    Job Description
                  </CardTitle>
                  <CardDescription>
                    Paste the job description you're applying for
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <Label htmlFor="job-description" className="sr-only">
                      Job Description
                    </Label>
                    <Textarea
                      id="job-description"
                      placeholder="Paste the complete job description here...

Include:
• Job title and company
• Required skills and qualifications
• Responsibilities
• Nice-to-have requirements"
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                      className="min-h-[200px] resize-none"
                    />
                    <p className="text-xs text-muted-foreground text-right">
                      {jobDescription.length} characters
                      {jobDescription.length < 50 && ' (minimum 50)'}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Processing Status */}
            {processingState !== 'idle' && (
              <div className="mb-8">
                <ProcessingStatus
                  status={processingState}
                  progress={progress}
                  message={statusMessage}
                />
              </div>
            )}

            {/* Action Button */}
            <div className="text-center">
              <Button
                size="lg"
                onClick={handleProcess}
                disabled={!canProcess || processingState === 'processing'}
                className="px-8 py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
              >
                {processingState === 'processing' ? (
                  <>
                    <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Tailor My Resume
                  </>
                )}
              </Button>
              {!canProcess && processingState === 'idle' && (
                <p className="text-sm text-muted-foreground mt-3">
                  {!resumeFile && 'Upload your resume'}
                  {resumeFile && jobDescription.length < 50 && 'Add more job description details'}
                </p>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            Powered by AI • Built with React & FastAPI
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
