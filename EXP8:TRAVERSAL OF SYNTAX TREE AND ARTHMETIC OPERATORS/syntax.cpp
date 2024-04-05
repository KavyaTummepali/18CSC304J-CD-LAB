#include <iostream>
#include <stack>
using namespace std;

struct TreeNode {
    char value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(char c) : value(c), left(nullptr), right(nullptr) {}
};

// Function to construct an expression tree from a postfix expression
TreeNode* constructExpressionTree(const string& postfix) {
    stack<TreeNode*> st;
    for (char ch : postfix) {
        if (isdigit(ch)) {
            st.push(new TreeNode(ch));
        } else {
            TreeNode* op2 = st.top(); st.pop();
            TreeNode* op1 = st.top(); st.pop();
            TreeNode* newNode = new TreeNode(ch);
            newNode->left = op1;
            newNode->right = op2;
            st.push(newNode);
        }
    }
    return st.top();
}

// Inorder traversal to print infix expression
void inorder(TreeNode* root) {
    if (!root) return;
    if (root->left) cout << "(";
    inorder(root->left);
    cout << root->value;
    inorder(root->right);
    if (root->right) cout << ")";
}

// Function to evaluate an expression tree
int evaluateExpressionTree(TreeNode* root) {
    if (!root) return 0;
    if (isdigit(root->value)) {
        return root->value - '0'; // Convert char to int
    }
    int leftVal = evaluateExpressionTree(root->left);
    int rightVal = evaluateExpressionTree(root->right);
    switch (root->value) {
        case '+': return leftVal + rightVal;
        case '-': return leftVal - rightVal;
        case '*': return leftVal * rightVal;
        case '/': return leftVal / rightVal;
        default: return 0; // Handle other operators if needed
    }
}

int main() {
    string postfixExpression = "34+5*";
    TreeNode* root = constructExpressionTree(postfixExpression);

    cout << "Infix expression: ";
    inorder(root);
    cout << endl;

    int result = evaluateExpressionTree(root);
    cout << "Result: " << result << endl;

    // Clean up memory (optional)
    // Implement a function to delete the tree nodes

    return 0;
}
