import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import type { CVSection } from '../types';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Skeleton } from './ui/skeleton';

interface SectionCardsProps {
  onQuestionClick: (question: string, section: string) => void;
}

const sectionIcons: Record<string, string> = {
  'Summary': 'fas fa-user-circle',
  'Experience': 'fas fa-briefcase',
  'Skills': 'fas fa-code',
  'Certificates': 'fas fa-certificate',
  'Languages': 'fas fa-globe',
  'Memberships': 'fas fa-users',
  'References': 'fas fa-address-book',
};

const sectionQuestions: Record<string, string[]> = {
  'Summary': [
    'Tell me about your background',
    'Core competencies'
  ],
  'Experience': [
    'What impact did you deliver at IOM?',
    'How did you apply DevOps practices?',
    'Tell me about your UNRWA experience'
  ],
  'Skills': [
    'What programming languages do you know?',
    'Cloud technologies experience'
  ],
  'Certificates': [
    'What certifications do you have?',
    'AWS expertise level'
  ],
  'Languages': [
    'What languages do you speak?',
    'Communication skills'
  ],
  'Memberships': [
    'Professional associations'
  ],
  'References': [
    'Who can provide references?'
  ]
};

export default function SectionCards({ onQuestionClick }: SectionCardsProps) {
  const { data: sections, isLoading, error } = useQuery({
    queryKey: ['/api/sections'],
    queryFn: () => api.getSections(),
  });

  if (isLoading) {
    return (
      <div className="space-y-4 overflow-y-auto chat-scroll pr-2">
        <div className="mb-6">
          <Skeleton className="h-8 w-48 mb-2" />
          <Skeleton className="h-4 w-96" />
        </div>
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="p-6">
            <CardContent className="p-0">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <Skeleton className="h-6 w-32 mb-2" />
                  <Skeleton className="h-4 w-full mb-1" />
                  <Skeleton className="h-4 w-3/4" />
                </div>
                <Skeleton className="h-6 w-6 ml-4" />
              </div>
              <div className="space-y-2">
                <Skeleton className="h-3 w-40 mb-2" />
                <div className="flex flex-wrap gap-2">
                  <Skeleton className="h-8 w-24" />
                  <Skeleton className="h-8 w-32" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4 overflow-y-auto chat-scroll pr-2">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-card-foreground mb-2">CV Sections</h2>
          <p className="text-muted-foreground">Browse different sections of the CV and ask questions</p>
        </div>
        <Card className="p-6">
          <CardContent className="p-0">
            <div className="text-center text-destructive">
              <i className="fas fa-exclamation-triangle text-2xl mb-2"></i>
              <p>Failed to load CV sections. Please try again later.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-4 overflow-y-auto chat-scroll pr-2">
      {/* Profile Overview Card */}
      <Card className="p-6 bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
        <CardContent className="p-0">
          <div className="flex items-start space-x-4">
            <div className="relative">
              <div className="w-20 h-20 rounded-full bg-gray-200 border-3 border-primary/30 flex items-center justify-center overflow-hidden">
                <img 
                  src="/sample.png" 
                  alt="Mohammed Alakhras" 
                  className="w-full h-full object-cover rounded-full"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                    e.currentTarget.nextElementSibling.style.display = 'flex';
                  }}
                />
                <div className="w-full h-full bg-gray-200 flex items-center justify-center text-gray-500 rounded-full" style={{display: 'none'}}>
                  <i className="fas fa-user text-3xl"></i>
                </div>
              </div>
            </div>
            
            <div className="flex-1">
              <h3 className="text-xl font-bold text-card-foreground mb-1">Mohammed Alakhras</h3>
              <p className="text-primary font-medium mb-2">Senior Information Management Officer</p>
              <p className="text-sm text-muted-foreground mb-3">
                Experienced professional with expertise in information management, data analysis, and system administration.
              </p>
              
              <div className="flex flex-wrap gap-3 text-xs">
                <div className="flex items-center space-x-1">
                  <i className="fas fa-map-marker-alt text-primary"></i>
                  <span>Amman, Jordan</span>
                </div>
                <div className="flex items-center space-x-1">
                  <i className="fas fa-briefcase text-primary"></i>
                  <span>8+ years experience</span>
                </div>
                <div className="flex items-center space-x-1">
                  <i className="fas fa-graduation-cap text-primary"></i>
                  <span>Master's degree</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-primary/20">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Quick Actions</p>
            <div className="flex flex-wrap gap-2">
              <Button
                variant="secondary"
                size="sm"
                className="px-3 py-1.5 text-sm"
                onClick={() => onQuestionClick("Tell me about your background and experience", "Summary")}
              >
                <i className="fas fa-user mr-2"></i>
                About Me
              </Button>
              <Button
                variant="secondary"
                size="sm"
                className="px-3 py-1.5 text-sm"
                onClick={() => onQuestionClick("What are your key technical skills?", "Skills")}
              >
                <i className="fas fa-code mr-2"></i>
                Skills
              </Button>
              <Button
                variant="secondary"
                size="sm"
                className="px-3 py-1.5 text-sm"
                onClick={() => onQuestionClick("What is your recent work experience?", "Experience")}
              >
                <i className="fas fa-briefcase mr-2"></i>
                Experience
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-card-foreground mb-2">CV Sections</h2>
        <p className="text-muted-foreground">Browse different sections of the CV and ask questions</p>
      </div>

      {sections?.map((section) => (
        <Card key={section.title} className="p-6 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-0">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-card-foreground mb-2">{section.title}</h3>
                <p className="text-sm text-muted-foreground line-clamp-3">
                  {section.excerpt}
                </p>
              </div>
              <i className={`${sectionIcons[section.title] || 'fas fa-file-alt'} text-primary text-xl ml-4`}></i>
            </div>
            
            <div className="space-y-2">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Suggested Questions</p>
              <div className="flex flex-wrap gap-2">
                {sectionQuestions[section.title]?.map((question, index) => (
                  <Button
                    key={index}
                    variant="secondary"
                    size="sm"
                    className="question-chip px-3 py-1.5 text-sm hover:bg-accent transition-colors"
                    onClick={() => onQuestionClick(question, section.title)}
                    data-testid={`button-question-${section.title.toLowerCase()}-${index}`}
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
