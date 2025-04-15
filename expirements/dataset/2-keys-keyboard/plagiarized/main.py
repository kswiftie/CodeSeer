class Solution:
    def minSteps(self, n: int) -> int:
        # If n is 1, no steps are needed
        if n == 1:
            return 0  # Return zero steps for input 1

        total_steps = 0  # Initialize total steps
        current_factor = 2  # Start with the smallest prime factor

        # Continue until n is reduced to 1
        while n > 1:
            # Check if current_factor divides n
            while n % current_factor == 0:
                total_steps += current_factor  # Add the factor to total steps
                n //= current_factor  # Reduce n by the factor

            current_factor += 1  # Move to the next factor

        # Return the total number of steps calculated
        return total_steps  # Final result