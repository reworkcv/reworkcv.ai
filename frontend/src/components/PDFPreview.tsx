import { FileText, Download, ExternalLink, ZoomIn, ZoomOut } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { useState } from 'react'

interface PDFPreviewProps {
  pdfUrl: string
  onDownload: () => void
}

export function PDFPreview({ pdfUrl, onDownload }: PDFPreviewProps) {
  const [zoom, setZoom] = useState(100)
  
  const openInNewTab = () => {
    window.open(pdfUrl, '_blank')
  }
  
  const increaseZoom = () => {
    setZoom(prev => Math.min(prev + 25, 200))
  }
  
  const decreaseZoom = () => {
    setZoom(prev => Math.max(prev - 25, 50))
  }
  
  const getPdfUrlWithZoom = () => {
    return `${pdfUrl}#view=FitH&zoom=${zoom}`
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="flex-shrink-0 flex flex-row items-center justify-between space-y-0 pb-4">
        <CardTitle className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary" />
          PDF Preview
        </CardTitle>
        <div className="flex items-center gap-2">
          <div className="flex items-center border rounded-md">
            <Button
              variant="ghost"
              size="sm"
              onClick={decreaseZoom}
              className="h-8 w-8 p-0 rounded-r-none"
            >
              <ZoomOut className="w-4 h-4" />
            </Button>
            <span className="px-2 text-sm font-medium min-w-[50px] text-center">
              {zoom}%
            </span>
            <Button
              variant="ghost"
              size="sm"
              onClick={increaseZoom}
              className="h-8 w-8 p-0 rounded-l-none"
            >
              <ZoomIn className="w-4 h-4" />
            </Button>
          </div>
          <Button variant="outline" size="sm" onClick={openInNewTab}>
            <ExternalLink className="w-4 h-4 mr-2" />
            Open
          </Button>
          <Button size="sm" onClick={onDownload}>
            <Download className="w-4 h-4 mr-2" />
            Download
          </Button>
        </div>
      </CardHeader>
      <CardContent className="flex-1 p-0">
        <div className="h-full bg-gray-100 rounded-b-xl overflow-auto">
          <iframe
            src={getPdfUrlWithZoom()}
            className="w-full border-0 pdf-iframe"
            title="Resume PDF Preview"
            style={{ 
              height: '100%',
              minHeight: '1000px'
            }}
          />
        </div>
      </CardContent>
    </Card>
  )
}
