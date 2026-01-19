import { Loader2, CheckCircle, XCircle } from 'lucide-react'
import { Progress } from './ui/progress'
import { Card, CardContent } from './ui/card'

interface ProcessingStatusProps {
  status: 'idle' | 'processing' | 'success' | 'error'
  progress: number
  message: string
}

const steps = [
  'Uploading documents...',
  'Converting to markdown...',
  'Parsing resume structure...',
  'Tailoring to job description...',
  'Generating LaTeX...',
  'Compiling PDF...',
]

export function ProcessingStatus({ status, progress, message }: ProcessingStatusProps) {
  if (status === 'idle') return null

  return (
    <Card className="border-2 border-primary/20 bg-primary/5">
      <CardContent className="pt-6">
        <div className="flex items-center gap-4 mb-4">
          {status === 'processing' && (
            <Loader2 className="w-6 h-6 text-primary animate-spin" />
          )}
          {status === 'success' && (
            <CheckCircle className="w-6 h-6 text-green-500" />
          )}
          {status === 'error' && (
            <XCircle className="w-6 h-6 text-red-500" />
          )}
          <div className="flex-1">
            <p className="font-medium">
              {status === 'processing' && 'Processing your resume...'}
              {status === 'success' && 'Resume tailored successfully!'}
              {status === 'error' && 'Error processing resume'}
            </p>
            <p className="text-sm text-muted-foreground">{message}</p>
          </div>
        </div>
        
        {status === 'processing' && (
          <>
            <Progress value={progress} className="h-2 mb-4" />
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {steps.map((step, index) => {
                const stepProgress = (index + 1) * (100 / steps.length)
                const isActive = progress >= stepProgress - (100 / steps.length) && progress < stepProgress
                const isComplete = progress >= stepProgress
                
                return (
                  <div
                    key={step}
                    className={`text-xs px-2 py-1 rounded-full text-center transition-colors ${
                      isComplete
                        ? 'bg-green-100 text-green-700'
                        : isActive
                        ? 'bg-primary/20 text-primary font-medium'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    {step.replace('...', '')}
                  </div>
                )
              })}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
