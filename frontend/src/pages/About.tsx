
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Book, Database, FlaskConical, Microscope, Dna } from "lucide-react";

const About = () => {
  return (
    <div className="container mx-auto py-12 px-4">
      <div className="mx-auto max-w-3xl">
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-gray-800">About Gene Gleaner</h1>
          <p className="text-lg text-gray-600">Extracting biology knowledge from the web</p>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Microscope className="h-6 w-6 text-biology" />
              What We Do
            </CardTitle>
            <CardDescription>Understanding our service</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p>
              Gene Gleaner is a specialized tool designed to help researchers, students, and biology enthusiasts extract relevant information from scientific articles and resources across the web.
            </p>
            <p>
              Our application uses natural language processing and pattern recognition to identify and extract biology-related content, saving you time and effort when researching complex topics.
            </p>
          </CardContent>
        </Card>

        <div className="grid gap-8 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Dna className="h-6 w-6 text-biology" />
                AI-Powered Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Our system uses advanced AI algorithms to identify and extract biology-related paragraphs, tables, and metadata from scientific articles. The AI has been trained on thousands of biology texts to recognize relevant information.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-6 w-6 text-biology" />
                Structured Data Extraction
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Gene Gleaner doesn't just copy text—it structures the information into a format that's easy to read, analyze, and incorporate into your own work. Tables, headlines, and key paragraphs are all neatly organized.
              </p>
            </CardContent>
          </Card>

          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FlaskConical className="h-6 w-6 text-biology" />
                For Scientists, By Scientists
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Developed by a team with backgrounds in both biology and computer science, Gene Gleaner is built to address the real needs of the scientific community. We understand the challenges of working with scientific literature and have designed our tool to make your research process more efficient.
              </p>
              <p className="mt-4">
                Whether you're studying genetics, cellular biology, ecology, or any other biology discipline, our tool can help you extract the information that matters most.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;
