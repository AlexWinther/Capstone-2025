import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
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
    title: "How brains beware: neural mechanisms of emotional attention",
    authors: "Patrik Vuilleumier",
    year: 2005,
    venue: "Trends in Cognitive Sciences (journal)",
    citations: 2072,
    fwci: 22,
    summary: "This paper explores the neural mechanisms underlying emotional attention, which is relevant to the foundational concept of 'attention' that inspired the 'Attention Is All You Need' architecture. While it focuses on biological rather than computational models, it provides insights into how brains prioritize emotionally salient information, informing the broader understanding of attention mechanisms.",
    link: "https://example.com/paper1",
    is_oa: false,
    rating: 0,
  },
  {
    id: 2,
    title: "Attention Is All You Need",
    authors: "Vaswani et al.",
    year: 2017,
    venue: "NeurIPS",
    citations: 98234,
    fwci: 15.5,
    summary: "Introduces the Transformer architecture, relying entirely on self-attention mechanisms.",
    link: "https://example.com/paper2",
    is_oa: true,
    rating: 0,
  },
];

export const ResearchResults = () => {
  const handleRatingChange = (paperId: number, rating: number) => {
    console.log(`Paper ${paperId} rated ${rating} stars`);
    // TODO: Connect to backend API
  };

  return (
    <div className="space-y-4">
      {mockPapers.map((paper) => (
        <Card key={paper.id} className="transition-shadow hover:shadow-md">
          <CardContent className="p-5">
            {/* Title row with metrics and rating */}
            <div className="flex justify-between items-start gap-4 mb-3">
              <h3 className="text-lg font-semibold text-primary flex-1 m-0">
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
                        paper.fwci >= 1.5 ? 'text-green-600' : 
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
            <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
              {paper.summary}
            </p>

            {/* Metadata */}
            <div className="space-y-2 mb-4">
              {paper.authors && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Users className="h-4 w-4" />
                  <span><strong>Authors:</strong> {paper.authors}</span>
                </div>
              )}
              {paper.year && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span><strong>Year:</strong> {paper.year}</span>
                </div>
              )}
              {paper.venue && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Building2 className="h-4 w-4" />
                  <span><strong>Venue:</strong> {paper.venue}</span>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2 flex-wrap">
              {paper.link && (
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-2 bg-muted hover:bg-muted/80"
                  onClick={() => window.open(paper.link, '_blank')}
                >
                  <Check className="h-4 w-4" />
                  Read Paper
                </Button>
              )}
              {paper.is_oa !== undefined && (
                <Button
                  variant="outline"
                  size="sm"
                  className={`gap-2 ${
                    paper.is_oa 
                      ? 'bg-green-600 text-white hover:bg-green-700' 
                      : 'bg-muted hover:bg-muted/80'
                  }`}
                >
                  {paper.is_oa ? (
                    <>
                      <ExternalLink className="h-4 w-4" />
                      Open Access
                    </>
                  ) : (
                    <>
                      <Lock className="h-4 w-4" />
                      Closed Access
                    </>
                  )}
                </Button>
              )}
              {paper.pdf_url && (
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-2 bg-blue-600 text-white hover:bg-blue-700"
                  onClick={() => window.open(paper.pdf_url, '_blank')}
                >
                  <FileText className="h-4 w-4" />
                  PDF
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
