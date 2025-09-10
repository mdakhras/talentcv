import { useState } from 'react';
import Header from '../components/Header';
import SectionCards from '../components/SectionCards';
import ChatPanel from '../components/ChatPanel';

export default function Home() {
  const [pendingQuestion, setPendingQuestion] = useState<string | undefined>();

  const handleQuestionClick = (question: string, section: string) => {
    setPendingQuestion(question);
  };

  const handleQuestionProcessed = () => {
    setPendingQuestion(undefined);
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-140px)]">
          <SectionCards onQuestionClick={handleQuestionClick} />
          <ChatPanel 
            pendingQuestion={pendingQuestion}
            onQuestionProcessed={handleQuestionProcessed}
          />
        </div>
      </main>
    </div>
  );
}
