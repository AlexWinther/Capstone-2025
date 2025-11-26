import { StarRating } from "@/components/ui/star-rating";
import { Users, Calendar, Building2, Check, Lock, ExternalLink, FileText } from "lucide-react";

interface Paper {
  id: number;
  title: string;
  authors?: string;
  year?: number;
  venue?: string;
  citations?: number;
  fwci?: number;
  summary: string;
  link?: string;
  is_oa?: boolean;
  pdf_url?: string;
  rating?: number;
}

const mockPapers: Paper[] = [
  {
    id: 1,
    title: "Electronic Health Records: Then, Now, and in the Future",
    authors: "R. Scott Evans",
    year: 2016,
    venue: "Yearbook of Medical Informatics (journal)",
    citations: 727,
    fwci: 43,
    summary: "This paper provides a comprehensive overview of electronic health records, their evolution, and future prospects in healthcare information systems.",
    link: "https://example.com/paper1",
    is_oa: true,
    pdf_url: "https://example.com/paper1.pdf",
    rating: 0,
  },
  {
    id: 2,
    title: "Neural Mechanisms of Involuntary Attention to Acoustic Novelty and Change",
    authors: "Risto Näätänen",
    year: 1998,
    venue: "Journal of Cognitive Neuroscience",
    citations: 910,
    fwci: 9.36,
    summary: "Investigates the neural mechanisms underlying involuntary attention to novel and changing acoustic stimuli, providing insights into attention processing.",
    link: "https://example.com/paper2",
    is_oa: false,
    rating: 0,
  },
  {
    id: 3,
    title: "Effective Approaches to Attention-based Neural Machine Translation",
    authors: "Minh-Thang Luong et al.",
    year: 2015,
    venue: "EMNLP",
    citations: 751,
    fwci: 0.00,
    summary: "This paper introduces attention mechanisms for neural machine translation, which later influenced the 'Attention Is All You Need' (2017) architecture.",
    link: "https://example.com/paper3",
    is_oa: false,
    rating: 0,
  },
  {
    id: 4,
    title: "Neural Mechanisms of Object-Based Attention",
    authors: "Steven J. Luck",
    year: 1994,
    venue: "Science",
    citations: 538,
    fwci: 22,
    summary: "Explores how the brain selectively attends to objects rather than spatial locations, revealing fundamental principles of visual attention.",
    link: "https://example.com/paper4",
    is_oa: false,
    rating: 0,
  },
];

export const ResearchResults = () => {
  const handleRatingChange = (paperId: number, rating: number) => {
    console.log(`Paper ${paperId} rated ${rating} stars`);
    // TODO: Connect to backend API
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {mockPapers.map((paper) => (
        <div
          key={paper.id}
          className="bg-card border border-border rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col"
        >
          {/* Title row with metrics and rating */}
          <div className="flex justify-between items-start gap-4 mb-3">
            <h3 className="text-lg font-semibold text-primary flex-1 m-0 leading-tight">
              {paper.title}
            </h3>
            
            <div className="flex items-center gap-4 flex-shrink-0">
              {/* Key Metrics */}
              <div className="flex gap-4">
                {paper.citations !== undefined && (
                  <div className="text-center">
                    <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide">
                      Citations
                    </div>
                    <div className="text-lg font-bold text-foreground">
                      {paper.citations.toLocaleString()}
                    </div>
                  </div>
                )}
                {paper.fwci !== undefined && (
                  <div className="text-center">
                    <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide">
                      FWCI
                    </div>
                    <div className={`text-lg font-bold ${
                      paper.fwci >= 1.5 ? 'text-accent' : 
                      paper.fwci >= 1.0 ? 'text-yellow-500' : 
                      'text-muted-foreground'
                    }`}>
                      {paper.fwci < 10 ? paper.fwci.toFixed(2) : Math.round(paper.fwci)}
                    </div>
                  </div>
                )}
              </div>

              {/* Star Rating */}
              <div className="pl-4 border-l-2 border-border">
                <StarRating
                  value={paper.rating || 0}
                  onChange={(value) => handleRatingChange(paper.id, value)}
                  readonly={false}
                />
              </div>
            </div>
          </div>

          {/* Summary */}
          <p className="text-sm text-muted-foreground mb-4 leading-relaxed flex-grow">
            {paper.summary}
          </p>

          {/* Metadata */}
          <div className="space-y-2 mb-4">
            {paper.authors && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Users className="h-4 w-4 flex-shrink-0" />
                <span><strong>Authors:</strong> {paper.authors}</span>
              </div>
            )}
            {paper.year && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Calendar className="h-4 w-4 flex-shrink-0" />
                <span><strong>Year:</strong> {paper.year}</span>
              </div>
            )}
            {paper.venue && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Building2 className="h-4 w-4 flex-shrink-0" />
                <span><strong>Venue:</strong> {paper.venue}</span>
              </div>
            )}
          </div>

          {/* Action Buttons - Fixed alignment */}
          <div className="flex items-center gap-2 flex-wrap mt-auto">
            {paper.link && (
              <button
                onClick={() => window.open(paper.link, '_blank')}
                className="inline-flex items-center justify-center gap-1.5 bg-muted hover:bg-muted/80 text-muted-foreground hover:text-foreground px-3 py-1.5 rounded-md text-xs font-semibold transition-colors h-7"
              >
                <Check className="h-3.5 w-3.5" />
                Read Paper
              </button>
            )}
            {paper.is_oa !== undefined && (
              <button
                className={`inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-colors h-7 ${
                  paper.is_oa 
                    ? 'bg-accent text-accent-foreground hover:bg-accent/90' 
                    : 'bg-muted hover:bg-muted/80 text-muted-foreground hover:text-foreground'
                }`}
              >
                {paper.is_oa ? (
                  <>
                    <ExternalLink className="h-3.5 w-3.5" />
                    Open Access
                  </>
                ) : (
                  <>
                    <Lock className="h-3.5 w-3.5" />
                    Closed Access
                  </>
                )}
              </button>
            )}
            {paper.pdf_url && (
              <button
                onClick={() => window.open(paper.pdf_url, '_blank')}
                className="inline-flex items-center justify-center gap-1.5 bg-primary hover:bg-primary/90 text-primary-foreground px-3 py-1.5 rounded-md text-xs font-semibold transition-colors h-7"
              >
                <FileText className="h-3.5 w-3.5" />
                PDF
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
