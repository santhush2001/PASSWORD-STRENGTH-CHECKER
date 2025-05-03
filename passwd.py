import re

def check_password_strength(password):
    """
    Check the strength of a password and return a score and feedback.
    
    Criteria:
    - Length (8+ chars)
    - Uppercase letters
    - Lowercase letters
    - Numbers
    - Special characters
    - Common patterns to avoid
    """
    
    score = 0
    feedback = []
    
    # Check length
    if len(password) >= 12:
        score += 3
        feedback.append("✓ Good length (12+ characters)")
    elif len(password) >= 8:
        score += 2
        feedback.append("✓ Minimum length (8+ characters)")
    else:
        feedback.append("✗ Too short (minimum 8 characters required)")
    
    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("✓ Contains uppercase letters")
    else:
        feedback.append("✗ No uppercase letters")
    
    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("✓ Contains lowercase letters")
    else:
        feedback.append("✗ No lowercase letters")
    
    # Check for numbers
    if re.search(r'[0-9]', password):
        score += 1
        feedback.append("✓ Contains numbers")
    else:
        feedback.append("✗ No numbers")
    
    # Check for special characters
    if re.search(r'[^A-Za-z0-9]', password):
        score += 2
        feedback.append("✓ Contains special characters")
    else:
        feedback.append("✗ No special characters")
    
    # Check for common weak patterns
    weak_patterns = [
        '123', 'abc', 'qwerty', 'password', 'admin', 'welcome', 
        '111', '000', 'iloveyou', 'letmein'
    ]
    
    if any(pattern in password.lower() for pattern in weak_patterns):
        score -= 2
        feedback.append("✗ Contains common weak patterns")
    
    # Determine strength level
    if score >= 7:
        strength = "Strong"
    elif score >= 5:
        strength = "Moderate"
    elif score >= 3:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    return strength, score, feedback

def main():
    print("Password Strength Checker")
    print("-------------------------")
    
    while True:
        password = input("\nEnter a password to check (or 'quit' to exit): ")
        
        if password.lower() == 'quit':
            break
            
        strength, score, feedback = check_password_strength(password)
        
        print(f"\nPassword Strength: {strength} (Score: {score}/8)")
        print("\nDetailed Feedback:")
        for item in feedback:
            print(f"- {item}")
        
        # Additional advice based on strength
        if strength in ["Very Weak", "Weak"]:
            print("\nRecommendation: Your password is too weak. Consider:")
            print("- Making it at least 12 characters long")
            print("- Adding uppercase letters, numbers, and special characters")
            print("- Avoiding common words or sequences")
        elif strength == "Moderate":
            print("\nRecommendation: Your password is okay but could be stronger.")
        else:
            print("\nRecommendation: Great! Your password is strong.")

if __name__ == "__main__":
    main()
