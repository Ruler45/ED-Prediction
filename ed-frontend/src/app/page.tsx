"use client";

import { Button } from "@/components/ui/button";
import { ModeToggle } from "@/components/ui/modeToggle";
import { Label } from "@radix-ui/react-label";
import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import axios from "axios";

type PredictionResult = {
  predicted_mass_deposition: number;
  predicted_hardness: number;
  predicted_sn_ratio: number;
  predicted_volume_fraction: number;
};

export default function Home() {
  const [current, setCurrent] = useState(1);
  const [ph, setPh] = useState(2.5);
  const [temperature, setTemperature] = useState(30);
  const [bathCon, setBathCon] = useState(10);
  const [speed, setSpeed] = useState(200);
  const [res, setRes] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handlePrdict = async (e: React.FormEvent) => {
    e.preventDefault();
    if (
      current === 0 ||
      ph === 0 ||
      temperature === 0 ||
      bathCon === 0 ||
      speed === 0
    ) {
      alert("Please fill all the fields to make a prediction.");
      return;
    }
    setLoading(true);

    // Here you would typically call an API to get the prediction
    // For demonstration, we will just log the values
    try {
      const data = {
        Current: current,
        pH: ph,
        Temp: temperature,
        Bath_conc: bathCon,
        Speed: speed,
      };

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/predict`,
        data,
      );
      // console.log(response.data);

      setRes(response.data);
    } catch (error) {
      console.error("Error making prediction:", error);
      alert("An error occurred while making the prediction. Please try again.");
      return;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col  items-center justify-items-center min-h-screen pb-4  gap-4 sm:p-2 font-[family-name:var(--font-geist-sans)] ">
      <nav>
        <ModeToggle />
      </nav>
      <div className="text-2xl"> Welcome!</div>
      <p className="text-xl">
        Here you can make predictions s on effect of process parameters of
        electrodeposited Ni-Al2O3
      </p>
      <div className=" bg-white dark:bg-gray-800">
        <form
          onSubmit={(e) => handlePrdict(e)}
          className="w-full max-w-2xl border p-4 rounded-lg shadow-md gap-2 flex flex-col"
        >
          <div>
            <div className="w-full flex justify-center fle-col">
              Enter the parameters below
            </div>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="name" className="text-right">
                  Current (A/dm<sup>2</sup>)
                </Label>
                <Select onValueChange={(value) => setCurrent(Number(value))}>
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="1" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1</SelectItem>
                    <SelectItem value="2">2</SelectItem>
                    <SelectItem value="3">3</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="description" className="text-right">
                  pH
                </Label>
                <Select onValueChange={(value) => setPh(Number(value))}>
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="2.5" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2.5">2.5</SelectItem>
                    <SelectItem value="3.5">3.5</SelectItem>
                    <SelectItem value="4.5">4.5</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="link" className="text-right">
                  Temperature (&deg;C)
                </Label>
                <Select
                  onValueChange={(value) => setTemperature(Number(value))}
                >
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="30" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="30">30</SelectItem>
                    <SelectItem value="45">45</SelectItem>
                    <SelectItem value="60">60</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="link" className="text-right">
                  Bath con. (g/l)
                </Label>
                <Select onValueChange={(value) => setBathCon(Number(value))}>
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="10" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="10">10</SelectItem>
                    <SelectItem value="20">20</SelectItem>
                    <SelectItem value="30">30</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="link" className="text-right">
                  Stirring speed (rpm)
                </Label>
                <Select onValueChange={(value) => setSpeed(Number(value))}>
                  <SelectTrigger className="col-span-3">
                    <SelectValue placeholder="200" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="200">200</SelectItem>
                    <SelectItem value="250">250</SelectItem>
                    <SelectItem value="300">300</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Note: The values you enter will be used to predict the mass
            deposited and hardness of the electrodeposited Ni-Al2O3.
          </div>
          <Button type="submit">Predict</Button>
          {/* <div>
            <span className="text-sm text-red-500 dark:text-red-400 &:hover:text-white-600">
              * Values of all parameters are required for prediction.
            </span>
          </div> */}
        </form>
        <div className="w-full bg-white dark:bg-gray-600 flex flex-col p-4 rounded-lg shadow-md mt-4">
          <span>Results:</span>
          {loading ? (
            <div className="text-center">Loading...</div>
          ) : res != null ? (
            <div>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-right">Mass deposited:</div>
                <div className="text-left">
                  {res.predicted_mass_deposition.toFixed(2)} mg
                </div>

                <div className="text-right">Hardness:</div>
                <div className="text-left">
                  {res.predicted_hardness.toFixed(2)} HV
                </div>

                <div className="text-right">S/N Ratio:</div>
                <div className="text-left">
                  {res.predicted_sn_ratio.toFixed(2)}
                </div>

                <div className="text-right">Volume Fraction:</div>
                <div className="text-left">
                  {res.predicted_volume_fraction.toFixed(2)} %
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
