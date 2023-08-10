bool is_leap_year(int year) {
    return (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));
}

// Calculate the number of days in a month
int days_in_month(int year, int month) {
    static const int days_in_month[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (month == 1 && is_leap_year(year)) {
        return 29;
    }
    return days_in_month[month];
}

// Convert a time structure to a timestamp
uint32_t struct_to_timestamp(const struct my_tm *time_struct) {
    int year = time_struct->year;
    int month = time_struct->month - 1; // Month is 0-based
    int day = time_struct->day;
    int hour = time_struct->hour;
    int minute = time_struct->minute;
    int second = time_struct->second;

    // Calculate the number of days since Jan 1, 1970
    int days_since_epoch = 0;
    for (int y = 1970; y < year; y++) {
        days_since_epoch += is_leap_year(y) ? 366 : 365;
    }
    for (int m = 0; m < month; m++) {
        days_since_epoch += days_in_month(year, m);
    }
    days_since_epoch += day - 1;

    // Calculate the total number of seconds
    uint32_t timestamp = days_since_epoch * 86400; // 86400 seconds per day
    timestamp += hour * 3600 + minute * 60 + second;

    return timestamp;
}

void timestamp_to_struct(uint32_t timestamp, struct my_tm *result) {
    // Calculate seconds, minutes, hours, days, etc.
    uint32_t total_seconds = timestamp;
    result->second = total_seconds % 60;
    total_seconds /= 60;
    result->minute = total_seconds % 60;
    total_seconds /= 60;
    result->hour = total_seconds % 24;
    total_seconds /= 24;

    // Calculate days since Jan 1, 1970
    int days_since_epoch = total_seconds;

    // Calculate year, month, day
    int year = 1970;
    int days_in_year;

    while (1) {
        days_in_year = is_leap_year(year) ? 366 : 365;

        if (days_since_epoch < days_in_year) {
            break;
        }

        days_since_epoch -= days_in_year;
        year++;
    }

    result->year = year;

    // Array of days in each month
    int month;
    for (month = 0; month < 12; month++) {
        int days_in_this_month = days_in_month(year, month);
        if (days_since_epoch < days_in_this_month) {
            break;
        }
        days_since_epoch -= days_in_this_month;
    }

    result->month = month + 1;
    result->day = days_since_epoch + 1;
}

