function PlotMSL(pattern)
    [maxima , maxpos] = max(pattern ,[], 'omitnan');
    for f = 1:size(pattern,2)
        if isnan(maxima(f))
            maxpos(f) = NaN;
        end
    end

    frequencys = find(~isnan(maxpos));
    Nfreq = size(frequencys, 2);

    MSL = NaN(1, max(frequencys));

    for f = 1:Nfreq
        pks = findpeaks(pattern(:,f));
        pks = sort(pks, 'descend');

        if size(pks,1) > 1
            MSL(frequencys(f)) = pks(1)-pks(2);
        else
            MSL(frequencys(f)) = NaN;
        end
    end

    plot(MSL);
end

