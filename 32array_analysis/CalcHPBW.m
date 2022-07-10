function HPBW = CalcHPBW(pattern)
    [maxima, maxpos] = max(pattern, [], 'omitnan');

    for f = 1:size(pattern, 2)
        if isnan(maxima(f))
            maxpos(f) = NaN;
        end
    end

frequencys = find(~isnan(maxpos));

Nfreq = size(frequencys, 2);

HPBW = NaN(1, max(frequencys));

for f = 1:Nfreq
    found = false;
    pos = maxpos(frequencys(f));

    while found == false
        value = (pattern(maxpos(frequencys(f)), frequencys(f)))-(pattern(pos, frequencys(f)));
        if round(value) >= 3
            HPBW(frequencys(f)) = 2*(maxpos(frequencys(f))-pos);
            found = true
        else
            pos = pos - 1
        end

        if pos == 0
            found = true;
            HPBW(frequencys(f)) = NaN;
        end
    end
end
end



