"use client";

import Link from "next/link";
import { useState } from "react";
import useSWR, { mutate } from "swr";
import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  Card,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  DropdownMenuTrigger,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuItem,
  DropdownMenuContent,
  DropdownMenu,
} from "@/components/ui/dropdown-menu";

async function fetcher(url: string) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error("Failed to fetch");
  }
  return res.json();
}

export default function ConfigPage() {
  const { data: config, error } = useSWR(
    "http://localhost:3000/config.json",
    fetcher,
  );

  const { data: defaultConfig, error: defaultConfigError } = useSWR(
    "http://localhost:3000/default_config.json",
  );

  const [values, setValues] = useState(config || {});

  const handleChange =
    (key: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setValues({
        ...values,
        [key]: event.target.value,
      });
    };

  const handleReset = async () => {
    if (!defaultConfig) return;

    for (const key in config) {
      const defaultValue =
        defaultConfig[key] !== undefined ? defaultConfig[key] : "";
      const res = await fetch("http://localhost:3000/api/config", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ key, value: defaultValue }),
      });

      if (res.ok) {
        setValues({ ...values, [key]: defaultValue });
        mutate("http://localhost:3000/config.json", {
          ...config,
          [key]: defaultValue,
        });
      } else {
        throw new Error("Failed to reset config");
      }
    }
  };

  const handleSubmit =
    (key: string) => async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      const res = await fetch(`http://localhost:3000/api/config`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ key, value: values[key] }),
      });

      if (res.ok) {
        alert("Update was successful.");
        setValues({ ...values, [key]: "" });
        mutate("http://localhost:3000/config.json", {
          ...config,
          [key]: values[key],
        });
      } else {
        throw new Error("Failed to update config");
      }
    };

  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  if (error) return <div>Error: {error.message}</div>;
  if (!config) return <div>Loading...</div>;

  return (
    <>
      <header className="flex items-center h-16 px-4 border-b shrink-0 md:px-6">
        <Link
          className="flex items-center gap-2 text-lg font-semibold sm:text-base mr-4"
          href="#"
        >
          <FrameIcon className="w-6 h-6" />
          <span className="sr-only">Acme Inc</span>
        </Link>
        <nav className="hidden font-medium sm:flex flex-row items-center gap-5 text-sm lg:gap-6">
          <Link className="font-bold" href="#">
            Devices
          </Link>
          <Link className="text-gray-500 dark:text-gray-400" href="#">
            Settings
          </Link>
          <Link className="text-gray-500 dark:text-gray-400" href="#">
            Users
          </Link>
        </nav>
        <div className="flex items-center w-full gap-4 md:ml-auto md:gap-2 lg:gap-4">
          <form className="flex items-center gap-2 md:gap-4 lg:gap-8 ml-auto">
            <Label className="hidden" htmlFor="search">
              Search
            </Label>
            <Input
              className="sm:w-[200px] md:w-[250px] lg:w-[300px] xl:w-[350px] 2xl:w-[400px] order-last"
              id="search"
              placeholder="Search..."
              type="search"
            />
            <Button size="icon" type="submit" variant="ghost">
              <SearchIcon className="h-4 w-4" />
              <span className="sr-only">Search</span>
            </Button>
          </form>
          <DropdownMenu>
            <Button
              className={`rounded-full border w-8 h-8 ${
                darkMode ? "border-gray-800" : "border-gray-200"
              }`}
              size="icon"
              variant="ghost"
              onClick={toggleDarkMode}
            >
              <img
                alt="Avatar"
                className="rounded-full"
                height="32"
                src="/placeholder.svg"
                style={{
                  aspectRatio: "32/32",
                  objectFit: "cover",
                }}
                width="32"
              />
              <span className="sr-only">Toggle user menu</span>
            </Button>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuItem>Support</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Logout</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
      <main>
        <div className="flex min-h-screen w-full bg-gray-100/40 dark:bg-gray-800/40">
          <div className="hidden w-[300px] border-r border-gray-200 md:block dark:border-gray-800">
            <nav className="flex flex-col gap-0.5 text-sm py-2.5">
              <Link
                className="flex items-center gap-3.5 rounded-r-xl px-3.5 py-2.5 bg-gray-100 text-gray-900 dark:bg-gray-900 dark:text-gray-100"
                href="#"
              >
                <WifiIcon className="h-4 w-4" />
                Network
              </Link>
              <Link
                className="flex items-center gap-3.5 rounded-r-xl px-3.5 py-2.5"
                href="#"
              >
                <LockIcon className="h-4 w-4" />
                Security
              </Link>
              <Link
                className="flex items-center gap-3.5 rounded-r-xl px-3.5 py-2.5"
                href="#"
              >
                <SettingsIcon className="h-4 w-4" />
                Device Parameters
              </Link>
              <Link
                className="flex items-center gap-3.5 rounded-r-xl px-3.5 py-2.5"
                href="#"
              >
                <DownloadIcon className="h-4 w-4" />
                Firmware Updates
              </Link>
            </nav>
          </div>
          <div className="flex flex-1 flex-col p-4 md:p-6 gap-4 md:gap-8">
            <div className="grid gap-4 md:gap-8">
              {Object.keys(config).map((key) => (
                <Card key={key}>
                  <CardHeader>
                    <CardTitle>{key}</CardTitle>
                    <CardDescription>Set the {key}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <form
                      className="flex items-center gap-4 md:gap-8"
                      onSubmit={handleSubmit(key)}
                    >
                      {/*
              <Label className="peer-hidden" htmlFor={key}>
                {key}
              </Label>
*/}
                      <Input
                        className="w-full max-w-[750px] peer-hidden"
                        id={key}
                        value={values[key]}
                        onChange={handleChange(key)}
                        placeholder={config[key]}
                        type="text"
                      />
                      <Button type="submit">Save</Button>
                      <Button size="sm" variant="outline" onClick={handleReset}>
                        Reset
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </main>
    </>
  );
}

function ChevronLeftIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m15 18-6-6 6-6" />
    </svg>
  );
}

function FrameIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="22" x2="2" y1="6" y2="6" />
      <line x1="22" x2="2" y1="18" y2="18" />
      <line x1="6" x2="6" y1="2" y2="22" />
      <line x1="18" x2="18" y1="2" y2="22" />
    </svg>
  );
}

function SearchIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}
function DownloadIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" x2="12" y1="15" y2="3" />
    </svg>
  );
}

function LockIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
  );
}

function SettingsIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}

function WifiIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5 13a10 10 0 0 1 14 0" />
      <path d="M8.5 16.5a5 5 0 0 1 7 0" />
      <path d="M2 8.82a15 15 0 0 1 20 0" />
      <line x1="12" x2="12.01" y1="20" y2="20" />
    </svg>
  );
}
