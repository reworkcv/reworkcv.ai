import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from './ui/button'

interface FileUploadProps {
  file: File | null
  onFileChange: (file: File | null) => void
  accept: Record<string, string[]>
  label: string
  description: string
}

export function FileUpload({ 
  file, 
  onFileChange, 
  accept, 
  label, 
  description 
}: FileUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileChange(acceptedFiles[0])
    }
  }, [onFileChange])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    multiple: false,
  })

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation()
    onFileChange(null)
  }

  return (
    <div
      {...getRootProps()}
      className={cn(
        "relative border-2 border-dashed rounded-xl p-8 transition-all duration-200 cursor-pointer",
        "hover:border-primary/50 hover:bg-primary/5",
        isDragActive && "border-primary bg-primary/10",
        file && "border-green-500/50 bg-green-50"
      )}
    >
      <input {...getInputProps()} />
      
      {file ? (
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <FileText className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="font-medium text-green-700">{file.name}</p>
              <p className="text-sm text-green-600">
                {(file.size / 1024).toFixed(1)} KB
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={removeFile}
            className="text-gray-400 hover:text-red-500"
          >
            <X className="w-5 h-5" />
          </Button>
        </div>
      ) : (
        <div className="text-center">
          <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
            <Upload className="w-6 h-6 text-primary" />
          </div>
          <p className="font-medium text-foreground mb-1">{label}</p>
          <p className="text-sm text-muted-foreground">{description}</p>
          {isDragActive && (
            <p className="text-sm text-primary mt-2 font-medium">
              Drop the file here...
            </p>
          )}
        </div>
      )}
    </div>
  )
}
