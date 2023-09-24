#include <stdio.h>

int main() {
    double initialInvestment, finalValue, roi;

    // Input initial investment and final value from the user
    printf("Enter the initial investment: $");
    scanf("%lf", &initialInvestment);

    printf("Enter the final value: $");
    scanf("%lf", &finalValue);

    // Calculate the ROI
    roi = ((finalValue - initialInvestment) / initialInvestment) * 100;

    // Display the ROI
    printf("The Return on Investment (ROI) is: %.2lf%%\n", roi);

    return 0;
}
