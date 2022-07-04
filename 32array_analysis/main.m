%{
    @title: Acoustic Camera
    @author: Luca Dommel
    @description: An Acoustic Camera with an rectangle Microphone Array
                  using Delay and Sum Algorithm
@sources: Leon Müller - Development of a Real-Time, Low-Budget Acoustic Camera on an FPGA
download website: https://www.researchgate.net/publication/350285885_Development_of_a_Real-Time_Low-Budget_Acoustic_Camera_on_an_FPGA
%}
%% 0.) CONSTANTS
c = 343.2; % speed of sound
frequenzy = 1000;
samplerate = 48000.0;
arrayDataFileName ='ArrayAnalysis/ArrayData.txt';
%% 1. Create Microphone Array via json
fileName = 'data/MicrophoneArrayData.json'; % filename in JSON extension
fid = fopen(fileName); % Opening the file
raw = fread(fid,inf); % Reading the contents
str = char(raw'); % Transformation
fclose(fid); % Closing the file
metaData = jsondecode(str); 
numChannels = length(metaData.elements);
for m = 1:numChannels
    arrayPoints(m,1) = metaData.elements(m).x;
    arrayPoints(m,2) = metaData.elements(m).y;
    arrayPoints(m,3) = metaData.elements(m).z;
end

xPos = arrayPoints(:,1);
yPos = arrayPoints(:,2);
zPos = zeros(numChannels,1);

%% 1.1 Analyse Microphone Array
figure("Name",'Microphone Array Geometry (in meter)')
array = scatter(arrayPoints(:,1), arrayPoints(:,2));
title('Microphone Array Geometry (in meter)')
saveas(array,'ArrayAnalysis/MicArray.png');

%calculates minimum and maximum possible spatial samplable frequency
[fmin, fmax] = CalcFrequencys(arrayPoints, c);

%calculates the Coarray of rectangle 32 mic array
[rm, coarray] = PlotCoArray(arrayPoints);
title('Microphone Co-Array Geometry (in meter)');
saveas(coarray,'ArrayAnalysis/CoArray.png');

%calculates beampattern of a steering direction
%   Berechnung des Strahlenmusters für eine bestimmte Array-Geometrie
%    ang = [45;0];
%    SteeringDirection = [0;90];
[bw, angle] = PlotBeampattern(arrayPoints,c, frequenzy);

%HPBW = CalcHPBW(pattern);
%MSL =  CalcMSL(pattern);
%Additional Analysis Data:
%HPBW - Half Power Beamwidth
%MSL - Maximum Side-lobe Level
%visualizing missing


%% 2. Microphone Data to  -> merged .wavs or .h file
%fid = fopen('data/MicrophoneArrayData.wav','rb');
%data=fread(fid,[numChannels sampleRate*numChannels],'int16');
%% 3. Build Plane-Grid
%% 4. Delay And Sum
%% 5. Create Pictures
%% 6. Create Video

%% Safe Analysis Data
arrayDataFile = fopen(arrayDataFileName,'w');
fprintf(arrayDataFile, 'Array Analysis Data of %2i-Mic-Array: \r\n\r\n', numChannels); 
fprintf(arrayDataFile, 'MinFrequenzy: %f Hz\n', fmin); 
fprintf(arrayDataFile, 'MaxFrequenzy: %f Hz\n', fmax); 
fprintf(arrayDataFile,'Medium Redundancy: %f\r\n',rm);
fprintf(arrayDataFile,'Beamwidth: %f (in degrees)\r\n',bw);
fprintf(arrayDataFile,'Angles: %f, %f (in degrees)\r\n',angle(1), angle(2));
fclose(arrayDataFile);


