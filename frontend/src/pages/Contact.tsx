
import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ContactIcon, Mail, User } from "lucide-react";
import { toast } from "sonner";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

// Define the form schema
const formSchema = z.object({
  name: z.string().min(2, { message: "Name must be at least 2 characters" }),
  email: z.string().email({ message: "Please enter a valid email address" }),
  message: z.string().min(10, { message: "Message must be at least 10 characters" })
});

type ContactFormValues = z.infer<typeof formSchema>;

const Contact = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Initialize the form
  const form = useForm<ContactFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      message: ""
    }
  });

  // Handle form submission
  const onSubmit = (data: ContactFormValues) => {
    setIsSubmitting(true);
    
    // Simulate API call with timeout
    setTimeout(() => {
      console.log("Form submitted:", data);
      toast.success("Message sent successfully! We'll get back to you soon.");
      form.reset();
      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <div className="container mx-auto py-12 px-4">
      <div className="mx-auto max-w-2xl">
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-gray-800">Contact Us</h1>
          <p className="text-lg text-gray-600">Get in touch with our team</p>
        </div>

        <Card className="shadow-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ContactIcon className="h-6 w-6 text-biology" />
              Send us a message
            </CardTitle>
            <CardDescription>
              We'll respond to your inquiry as soon as possible
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Name</FormLabel>
                      <FormControl>
                        <div className="relative">
                          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                            <User size={18} />
                          </div>
                          <Input className="pl-10" placeholder="Your name" {...field} />
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <div className="relative">
                          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                            <Mail size={18} />
                          </div>
                          <Input className="pl-10" type="email" placeholder="Your email address" {...field} />
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="message"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Message</FormLabel>
                      <FormControl>
                        <textarea 
                          className="flex h-32 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                          placeholder="Your message here..."
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <Button 
                  type="submit" 
                  className="w-full bg-biology hover:bg-biology-dark"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Sending..." : "Send Message"}
                </Button>
              </form>
            </Form>
          </CardContent>
          <CardFooter className="flex-col items-start border-t bg-gray-50 px-6 py-4">
            <h4 className="mb-2 font-medium">Other ways to reach us:</h4>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Mail className="h-4 w-4" />
              <span>support@genegleaner.com</span>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default Contact;
