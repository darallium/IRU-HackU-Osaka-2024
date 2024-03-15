import Link from "next/link";
import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  CardFooter,
  Card,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { getConfig } from "@/utils/configUtils";

const generateFormElements = (config) => {
  return Object.keys(config).map((key) => (
    <div key={key} className="flex items-center gap-4">
      <label className="w-20" htmlFor={key}>
        {key}
      </label>
      <Input
        className="w-full"
        id={key}
        placeholder={`${config[key]}`}
        type="text"
      />
    </div>
  ));
};

export default function Component() {
  const config = getConfig();

  return (
    <div className="flex min-h-screen w-full bg-gray-100/40 dark:bg-gray-800/40">
      <div className="hidden w-[300px] border-r border-gray-200 md:block dark:border-gray-800">
        <nav className="flex flex-col gap-0.5 text-sm py-2.5">
          {/* Add your navigation links here */}
        </nav>
      </div>
      <div className="flex-1 grid gap-4 p-4 md:gap-8 md:p-10">
        <div className="flex items-center gap-4">
          {/* Add your title and icon here */}
        </div>
        <div className="grid gap-4 md:grid-cols-[1fr_1fr]">
          <Card className="grid gap-2">
            <CardHeader>
              <CardTitle>{/* Add your card title here */}</CardTitle>
              <CardDescription>
                {/* Add your card description here */}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form className="grid gap-4 md:grid-cols-[1fr_1fr]">
                {generateFormElements(config.default_config)}
              </form>
            </CardContent>
            <CardFooter className="flex gap-4">
              <Button size="sm">{/* Add your button label here */}</Button>
              <Button size="sm" variant="outline">
                {/* Add your advanced button label here */}
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}

/*
import Link from "next/link";
import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  CardFooter,
  Card,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { getConfig } from "@/utils/configUtils"; // Import the getConfig function

export default function Component() {
  const config = getConfig(); // Get config values

  return (
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
      <div className="flex-1 grid gap-4 p-4 md:gap-8 md:p-10">
        <div className="flex items-center gap-4">
          <WifiIcon className="h-6 w-6" />
          <h1 className="font-semibold text-lg md:text-2xl">Network</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-[1fr_1fr]">
          <Card className="grid gap-2">
            <CardHeader>
              <CardTitle>Wi-Fi Network</CardTitle>
              <CardDescription>
                Connect to a Wi-Fi network to enable internet access.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form className="grid gap-4 md:grid-cols-[1fr_1fr]">
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="ssid">
                    SSID
                  </label>
                  <Input
                    className="w-full"
                    id="ssid"
                    placeholder="Enter SSID"
                  />
                </div>
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="password">
                    Password
                  </label>
                  <Input
                    className="w-full"
                    id="password"
                    placeholder="Enter password"
                    type="password"
                  />
                </div>
              </form>
            </CardContent>
            <CardFooter className="flex gap-4">
              <Button size="sm">Connect</Button>
              <Button size="sm" variant="outline">
                Advanced
              </Button>
            </CardFooter>
          </Card>
          <Card className="grid gap-2">
            <CardHeader>
              <CardTitle>IP Address</CardTitle>
              <CardDescription>
                View the device's IP address and configure network settings.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form className="grid gap-4 md:grid-cols-[1fr_1fr]">
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="ip">
                    IP Address
                  </label>
                  <Input
                    className="w-full"
                    id="ip"
                    placeholder="Enter IP Address"
                  />
                </div>
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="subnet">
                    Subnet
                  </label>
                  <Input
                    className="w-full"
                    id="subnet"
                    placeholder="Enter Subnet"
                  />
                </div>
              </form>
            </CardContent>
            <CardFooter className="flex gap-4">
              <Button size="sm">Save</Button>
              <Button size="sm" variant="outline">
                Reset
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}
*/

/*
import Link from "next/link";
import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  CardFooter,
  Card,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Component() {
  return (
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
      <div className="flex-1 grid gap-4 p-4 md:gap-8 md:p-10">
        <div className="flex items-center gap-4">
          <WifiIcon className="h-6 w-6" />
          <h1 className="font-semibold text-lg md:text-2xl">Network</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-[1fr_1fr]">
          <Card className="grid gap-2">
            <CardHeader>
              <CardTitle>Wi-Fi Network</CardTitle>
              <CardDescription>
                Connect to a Wi-Fi network to enable internet access.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form className="grid gap-4 md:grid-cols-[1fr_1fr]">
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="ssid">
                    SSID
                  </label>
                  <Input
                    className="w-full"
                    id="ssid"
                    placeholder="Enter SSID"
                  />
                </div>
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="password">
                    Password
                  </label>
                  <Input
                    className="w-full"
                    id="password"
                    placeholder="Enter password"
                    type="password"
                  />
                </div>
              </form>
            </CardContent>
            <CardFooter className="flex gap-4">
              <Button size="sm">Connect</Button>
              <Button size="sm" variant="outline">
                Advanced
              </Button>
            </CardFooter>
          </Card>
          <Card className="grid gap-2">
            <CardHeader>
              <CardTitle>IP Address</CardTitle>
              <CardDescription>
                View the device's IP address and configure network settings.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form className="grid gap-4 md:grid-cols-[1fr_1fr]">
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="ip">
                    IP Address
                  </label>
                  <Input
                    className="w-full"
                    id="ip"
                    placeholder="Enter IP Address"
                  />
                </div>
                <div className="flex items-center gap-4">
                  <label className="w-20" htmlFor="subnet">
                    Subnet
                  </label>
                  <Input
                    className="w-full"
                    id="subnet"
                    placeholder="Enter Subnet"
                  />
                </div>
              </form>
            </CardContent>
            <CardFooter className="flex gap-4">
              <Button size="sm">Save</Button>
              <Button size="sm" variant="outline">
                Reset
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}
*/

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
