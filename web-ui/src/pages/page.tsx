"use client";

import { GetServerSideProps } from 'next';
import { CardTitle, CardDescription, CardHeader, CardContent, Card } from "@/components/ui/card";

export default function ConfigPage({ config }) {
  // If config is not yet loaded, show a loading message
  if (!config) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {Object.keys(config).map((key) => (
        <Card key={key}>
          <CardHeader>
            <CardTitle>{key}</CardTitle>
            <CardDescription>{JSON.stringify(config[key], null, 2)}</CardDescription>
          </CardHeader>
        </Card>
      ))}
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async () => {
  const res = await fetch('http://localhost:3000/config.json');
  const config = await res.json();

  return {
    props: {
      config,
    },
  };
};
