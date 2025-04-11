import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Book, Database, FlaskConical, Microscope, Dna } from "lucide-react";

const About = () => {
  return (
    <div className="container mx-auto py-12 px-4">
      <div className="mx-auto max-w-3xl">
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-gray-800">Cancer Biomarker Identification Platform</h1>
          <p className="text-lg text-gray-600">Advancing personalized medicine through biomarker discovery</p>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Microscope className="h-6 w-6 text-biology" />
              Our Mission
            </CardTitle>
            <CardDescription>Transforming cancer research through technology</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p>
              Our platform integrates cutting-edge machine learning with modern web technologies to create a comprehensive system for cancer biomarker identification, enabling early detection and improved treatment outcomes.
            </p>
            <p>
              By bridging computational biology with web technology, we empower researchers and clinicians to make significant strides in oncology, facilitating new discoveries in cancer research and precision medicine.
            </p>
          </CardContent>
        </Card>

        <div className="grid gap-8 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Dna className="h-6 w-6 text-biology" />
                Advanced ML Models
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Our Python-based Flask backend hosts state-of-the-art machine learning models that analyze complex biological datasets to accurately predict cancer biomarkers. We leverage libraries like Scikit-learn, TensorFlow, and Pandas for efficient data preprocessing and predictive analytics.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-6 w-6 text-biology" />
                Interactive Platform
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Our NextJS frontend delivers an intuitive user experience tailored for researchers and clinicians. Users can input various types of biological data, interact dynamically with our ML models, and visualize results through responsive interfaces without needing extensive computational expertise.
              </p>
            </CardContent>
          </Card>

          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FlaskConical className="h-6 w-6 text-biology" />
                Modular & Scalable Design
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                Our system is meticulously designed to be modular, scalable, and highly adaptable, making it capable of handling diverse datasets and addressing a wide array of use cases in cancer research.
              </p>
              <p className="mt-4">
                By predicting whether specific oncogenes will contribute to cancer onset, our platform empowers researchers to make significant advances in early detection strategies, personalized treatment plans, and groundbreaking oncology research.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;